"""Comments API endpoints."""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import DBSession, CurrentUser
from app.schemas.comment import CommentCreate, CommentResponse, CommentUpdate, CommentWithAuthor
from app.schemas.common import PaginatedResponse, PaginationMeta, DeleteResponse
from app.schemas.user import UserResponse
from app.models.comment import Comment
from app.models.card import Card
from app.models.user import User
from app.services.comment_service import CommentService
from app.services.activity_service import ActivityLogger

router = APIRouter()


@router.get("/cards/{card_id}/comments", response_model=PaginatedResponse[CommentWithAuthor])
def get_card_comments(
    card_id: uuid.UUID | str,
    db: DBSession,
    current_user: CurrentUser,
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 20,
    include_replies: Annotated[bool, Query(description="Include reply comments")] = True,
) -> PaginatedResponse[CommentWithAuthor]:
    """
    Get all comments for a specific card.

    Requires the user to have access to the board containing the card.
    """
    # Convert UUID to string for database compatibility
    card_id_str = str(card_id) if isinstance(card_id, uuid.UUID) else card_id

    # Verify card exists
    card = db.query(Card).filter(Card.id == card_id_str).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found",
        )

    # TODO: Add board access check here when implemented

    comments, total = CommentService.get_comments_for_card(
        db=db,
        card_id=card_id_str,
        page=page,
        page_size=page_size,
        include_replies=include_replies,
    )

    # Eager load author for each comment
    for comment in comments:
        db.refresh(comment, ["author"])

    comment_responses = [
        CommentWithAuthor(
            **CommentResponse.model_validate(comment).model_dump(),
            author=UserResponse.model_validate(comment.author),
        )
        for comment in comments
    ]

    return PaginatedResponse(
        success=True,
        data=comment_responses,
        pagination=PaginationMeta.create(page, page_size, total),
    )


@router.post("/cards/{card_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    card_id: uuid.UUID,
    comment_data: CommentCreate,
    db: DBSession,
    current_user: CurrentUser,
) -> CommentResponse:
    """
    Create a new comment on a card.

    Can optionally reply to an existing comment by providing parent_id.
    """
    # Verify card exists
    card_id_str = str(card_id) if isinstance(card_id, uuid.UUID) else card_id
    card = db.query(Card).filter(Card.id == card_id_str).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found",
        )

    # TODO: Add board access check here when implemented

    # Override card_id from URL to ensure consistency
    comment_data.card_id = card_id

    try:
        comment = CommentService.create_comment(
            db=db,
            card_id=card_id,
            user_id=current_user.id,
            content=comment_data.content,
            parent_id=comment_data.parent_id,
            log_activity=True,
        )
        return CommentResponse.model_validate(comment)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/comments/{comment_id}", response_model=CommentWithAuthor)
def get_comment(
    comment_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> CommentWithAuthor:
    """Get a specific comment by ID."""
    comment = CommentService.get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    # Eager load author
    db.refresh(comment, ["author"])

    return CommentWithAuthor(
        **CommentResponse.model_validate(comment).model_dump(),
        author=UserResponse.model_validate(comment.author),
    )


@router.get("/comments/{comment_id}/replies", response_model=PaginatedResponse[CommentWithAuthor])
def get_comment_replies(
    comment_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 20,
) -> PaginatedResponse[CommentWithAuthor]:
    """Get all replies to a specific comment."""
    # Verify parent comment exists
    parent_comment = CommentService.get_comment_by_id(db, comment_id)
    if not parent_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent comment not found",
        )

    replies, total = CommentService.get_replies(
        db=db,
        comment_id=comment_id,
        page=page,
        page_size=page_size,
    )

    # Eager load author for each reply
    for reply in replies:
        db.refresh(reply, ["author"])

    reply_responses = [
        CommentWithAuthor(
            **CommentResponse.model_validate(reply).model_dump(),
            author=UserResponse.model_validate(reply.author),
        )
        for reply in replies
    ]

    return PaginatedResponse(
        success=True,
        data=reply_responses,
        pagination=PaginationMeta.create(page, page_size, total),
    )


@router.put("/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: uuid.UUID,
    comment_data: CommentUpdate,
    db: DBSession,
    current_user: CurrentUser,
) -> CommentResponse:
    """Update a comment's content. Only the comment author can edit their own comments."""
    # Verify comment exists
    comment = CommentService.get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    # Check ownership
    if not CommentService.can_edit_comment(db, comment_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own comments",
        )

    try:
        updated_comment = CommentService.update_comment(
            db=db,
            comment_id=comment_id,
            user_id=current_user.id,
            content=comment_data.content,
            log_activity=True,
        )
        return CommentResponse.model_validate(updated_comment)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/comments/{comment_id}", response_model=DeleteResponse)
def delete_comment(
    comment_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> DeleteResponse:
    """Delete a comment. Only the comment author can delete their own comments."""
    # Verify comment exists
    comment = CommentService.get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    # Check ownership
    if not CommentService.can_delete_comment(db, comment_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own comments",
        )

    try:
        CommentService.delete_comment(
            db=db,
            comment_id=comment_id,
            user_id=current_user.id,
            log_activity=True,
        )
        return DeleteResponse(success=True, message="Comment deleted successfully")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

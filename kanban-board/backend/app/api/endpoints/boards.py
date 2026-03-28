"""Board API endpoints."""
import uuid
from typing import Annotated, Literal

from fastapi import APIRouter, Body, Depends, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import DBSession, CurrentUser
from app.schemas.board import (
    BoardCreate,
    BoardUpdate,
    BoardResponse,
    BoardWithMembers,
    BoardMemberRole,
)
from app.schemas.common import PaginationMeta, PaginatedResponse
from app.schemas.user import UserResponse
from app.models.board import Board
from app.models.board_member import BoardMember
from app.models.user import User
from app.services import board_service

router = APIRouter()


class UpdateMemberRoleRequest(BaseModel):
    """Request schema for updating member role."""

    role: Literal["owner", "admin", "member", "viewer"] = Field(
        ..., description="New role to assign to the member"
    )


@router.get("", response_model=PaginatedResponse[BoardResponse])
def get_boards(
    db: DBSession,
    current_user: CurrentUser,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    include_archived: bool = False,
) -> dict:
    """Get all boards for the current user."""
    boards, total = board_service.get_boards_for_user(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        include_archived=include_archived,
    )

    return {
        "success": True,
        "data": boards,
        "pagination": PaginationMeta.create(skip // limit + 1, limit, total),
    }


@router.post("", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
def create_board(
    board_data: BoardCreate,
    db: DBSession,
    current_user: CurrentUser,
) -> Board:
    """Create a new board."""
    return board_service.create_board(db, board_data, current_user.id)


@router.get("/{board_id}", response_model=BoardWithMembers)
def get_board(
    board_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> Board:
    """Get a board by ID with statistics and lists."""
    board = board_service.get_board_by_id(db, board_id, current_user.id)
    stats = board_service.get_board_stats(db, board_id)

    from app.models.list import List as ListModel
    from app.models.card import Card
    from app.services import list_service, card_service

    lists = list_service.get_lists_for_board(db, board_id, current_user.id)
    lists_data = []
    for lst in lists:
        cards = card_service.get_cards_for_list(db, lst.id)
        lists_data.append({
            "id": lst.id,
            "title": lst.title,
            "position": lst.position,
            "cards": [
                {
                    "id": card.id,
                    "title": card.title,
                    "description": card.description,
                    "position": card.position,
                    "priority": card.priority,
                    "due_date": card.due_date.isoformat() if card.due_date else None,
                    "assignee_id": card.assignee_id,
                    "is_completed": card.is_completed,
                    "created_at": card.created_at.isoformat(),
                    "updated_at": card.updated_at.isoformat(),
                }
                for card in cards
            ],
        })

    board_dict = BoardResponse.model_validate(board).model_dump()
    board_dict.update(stats)
    board_dict["lists"] = lists_data

    return board_dict


@router.put("/{board_id}", response_model=BoardResponse)
def update_board(
    board_id: uuid.UUID,
    board_data: BoardUpdate,
    db: DBSession,
    current_user: CurrentUser,
) -> Board:
    """Update a board."""
    return board_service.update_board(db, board_id, board_data, current_user.id)


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board(
    board_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> None:
    """Delete a board."""
    board_service.delete_board(db, board_id, current_user.id)


@router.get("/{board_id}/members", response_model=list[UserResponse])
def get_board_members(
    board_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> list[BoardMember]:
    """Get all members of a board."""
    # Check access
    board_service.check_board_access(db, board_id, current_user.id)

    members = db.query(BoardMember).filter(
        BoardMember.board_id == board_id
    ).all()

    # Get user objects
    user_ids = [m.user_id for m in members]
    users = db.query(User).filter(User.id.in_(user_ids)).all()

    return users


@router.post("/{board_id}/members", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def add_board_member(
    board_id: uuid.UUID,
    member_data: BoardMemberRole,
    db: DBSession,
    current_user: CurrentUser,
) -> User:
    """Add a member to a board."""
    member = board_service.add_board_member(db, board_id, member_data, current_user.id)

    # Return the user
    user = db.query(User).filter(User.id == member.user_id).first()
    return user


@router.delete("/{board_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_board_member(
    board_id: uuid.UUID,
    user_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> None:
    """Remove a member from a board."""
    board_service.remove_board_member(db, board_id, user_id, current_user.id)


@router.patch("/{board_id}/members/{user_id}", response_model=UserResponse)
def update_board_member_role(
    board_id: uuid.UUID,
    user_id: uuid.UUID,
    role_data: UpdateMemberRoleRequest,
    db: DBSession,
    current_user: CurrentUser,
) -> User:
    """Update a board member's role."""
    board_service.update_board_member_role(
        db, board_id, user_id, role_data.role, current_user.id
    )

    # Return the user
    user = db.query(User).filter(User.id == user_id).first()
    return user

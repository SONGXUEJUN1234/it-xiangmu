"""Activities API endpoints."""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import DBSession, CurrentUser
from app.schemas.activity import ActivityResponse, ActivityWithUser
from app.schemas.common import PaginatedResponse, PaginationMeta
from app.schemas.user import UserResponse
from app.models.activity import Activity
from app.models.board import Board
from app.services.activity_service import ActivityService

router = APIRouter()


@router.get("/boards/{board_id}/activities", response_model=PaginatedResponse[ActivityWithUser])
def get_board_activities(
    board_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 50,
    entity_type: Annotated[str | None, Query(description="Filter by entity type")] = None,
    user_id: Annotated[uuid.UUID | None, Query(description="Filter by user")] = None,
) -> PaginatedResponse[ActivityWithUser]:
    """
    Get activity history for a specific board.

    Supports filtering by entity type and user.
    Entity types: board, list, card, member, label, comment
    """
    # Verify board exists
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    # TODO: Add board access check here when implemented

    activities, total = ActivityService.get_activities_for_board(
        db=db,
        board_id=board_id,
        page=page,
        page_size=page_size,
        entity_type=entity_type,
        user_id=user_id,
    )

    # Eager load user for each activity
    for activity in activities:
        db.refresh(activity, ["user"])

    activity_responses = [
        ActivityWithUser(
            **ActivityResponse.model_validate(activity).model_dump(),
            user=UserResponse.model_validate(activity.user),
        )
        for activity in activities
    ]

    return PaginatedResponse(
        success=True,
        data=activity_responses,
        pagination=PaginationMeta.create(page, page_size, total),
    )


@router.get("/activities/{activity_id}", response_model=ActivityWithUser)
def get_activity(
    activity_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> ActivityWithUser:
    """Get a specific activity by ID."""
    activity = ActivityService.get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )

    # Eager load user
    db.refresh(activity, ["user"])

    return ActivityWithUser(
        **ActivityResponse.model_validate(activity).model_dump(),
        user=UserResponse.model_validate(activity.user),
    )


@router.get("/boards/{board_id}/activities/entities/{entity_type}/{entity_id}", response_model=PaginatedResponse[ActivityWithUser])
def get_entity_activities(
    board_id: uuid.UUID,
    entity_type: str,
    entity_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
    limit: Annotated[int, Query(ge=1, le=100, description="Maximum items to return")] = 50,
) -> PaginatedResponse[ActivityWithUser]:
    """
    Get all activities for a specific entity within a board.

    Entity types: board, list, card, member, label, comment
    """
    # Verify board exists
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    # Validate entity type
    valid_types = [
        ActivityService.ENTITY_BOARD,
        ActivityService.ENTITY_LIST,
        ActivityService.ENTITY_CARD,
        ActivityService.ENTITY_MEMBER,
        ActivityService.ENTITY_LABEL,
        ActivityService.ENTITY_COMMENT,
    ]
    if entity_type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid entity_type. Must be one of: {', '.join(valid_types)}",
        )

    activities = ActivityService.get_activities_for_entity(
        db=db,
        board_id=board_id,
        entity_type=entity_type,
        entity_id=entity_id,
        limit=limit,
    )

    # Eager load user for each activity
    for activity in activities:
        db.refresh(activity, ["user"])

    activity_responses = [
        ActivityWithUser(
            **ActivityResponse.model_validate(activity).model_dump(),
            user=UserResponse.model_validate(activity.user),
        )
        for activity in activities
    ]

    return PaginatedResponse(
        success=True,
        data=activity_responses,
        pagination=PaginationMeta.create(page=1, page_size=limit, total=len(activities)),
    )


# Helper endpoint to get activity statistics for a board
@router.get("/boards/{board_id}/activities/stats")
def get_board_activity_stats(
    board_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> dict:
    """
    Get activity statistics for a board.

    Returns counts by entity type and action.
    """
    # Verify board exists
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    from sqlalchemy import func

    stats = db.query(
        Activity.entity_type,
        Activity.action,
        func.count(Activity.id).label("count"),
    ).filter(
        Activity.board_id == board_id,
    ).group_by(
        Activity.entity_type,
        Activity.action,
    ).all()

    # Format results
    result = {
        "total_activities": sum(s.count for s in stats),
        "by_entity": {},
        "by_action": {},
    }

    for stat in stats:
        entity_type = stat.entity_type
        action = stat.action
        count = stat.count

        if entity_type not in result["by_entity"]:
            result["by_entity"][entity_type] = 0
        result["by_entity"][entity_type] += count

        if action not in result["by_action"]:
            result["by_action"][action] = 0
        result["by_action"][action] += count

    return result

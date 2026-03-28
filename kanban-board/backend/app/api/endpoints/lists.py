"""List API endpoints."""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import DBSession, CurrentUser
from app.schemas.list import ListCreate, ListUpdate, ListResponse, ListWithCards
from app.models.list import List as ListModel
from app.services import list_service

router = APIRouter()


class ReorderListsRequest(BaseModel):
    """Request schema for reordering lists."""

    list_positions: dict[uuid.UUID, int] = Field(
        ..., description="Dictionary mapping list IDs to their new positions"
    )


@router.get("/board/{board_id}", response_model=list[ListResponse])
def get_lists_for_board(
    board_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
    include_archived: bool = False,
) -> list[ListModel]:
    """Get all lists for a board."""
    return list_service.get_lists_for_board(
        db,
        board_id=board_id,
        user_id=current_user.id,
        include_archived=include_archived,
    )


@router.post("", response_model=ListResponse, status_code=status.HTTP_201_CREATED)
def create_list(
    list_data: ListCreate,
    db: DBSession,
    current_user: CurrentUser,
) -> ListModel:
    """Create a new list."""
    return list_service.create_list(db, list_data, current_user.id)


@router.get("/{list_id}", response_model=ListWithCards)
def get_list(
    list_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> ListModel:
    """Get a list by ID with cards count."""
    lst = list_service.get_list_by_id(db, list_id, current_user.id)
    cards_count = list_service.get_cards_count_for_list(db, list_id)

    # Convert to dict and add cards count
    list_dict = ListResponse.model_validate(lst).model_dump()
    list_dict["cards_count"] = cards_count

    return list_dict


@router.put("/{list_id}", response_model=ListResponse)
def update_list(
    list_id: uuid.UUID,
    list_data: ListUpdate,
    db: DBSession,
    current_user: CurrentUser,
) -> ListModel:
    """Update a list."""
    return list_service.update_list(db, list_id, list_data, current_user.id)


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(
    list_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> None:
    """Delete a list."""
    list_service.delete_list(db, list_id, current_user.id)


@router.post("/reorder", response_model=list[ListResponse])
def reorder_lists(
    request_data: ReorderListsRequest,
    board_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> list[ListModel]:
    """Reorder lists on a board."""
    return list_service.reorder_lists(
        db,
        board_id=board_id,
        list_positions=request_data.list_positions,
        user_id=current_user.id,
    )

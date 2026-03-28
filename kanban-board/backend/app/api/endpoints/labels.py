"""Label API endpoints."""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import DBSession, CurrentUser
from app.models.label import Label
from app.models.board import Board
from app.models.card import Card
from app.models.list import List
from app.schemas.label import (
    LabelCreate,
    LabelUpdate,
    LabelResponse,
)
from app.schemas.common import DeleteResponse
from app.services import label_service
from app.services import card_service

router = APIRouter()


def _verify_board_access(
    db: Session, board_id: uuid.UUID, user: uuid.UUID
) -> Board:
    """Verify user has access to the board.

    Args:
        db: Database session
        board_id: Board ID to verify
        user: Current user ID

    Returns:
        The board object

    Raises:
        HTTPException: If board not found or user doesn't have access
    """
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    if board.owner_id != user and not board.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this board",
        )

    return board


def _verify_card_access(
    db: Session, card_id: uuid.UUID, user_id: uuid.UUID
) -> Card:
    """Verify user has access to the card's board.

    Args:
        db: Database session
        card_id: Card ID to verify
        user_id: Current user ID

    Returns:
        The card object

    Raises:
        HTTPException: If card not found or user doesn't have access
    """
    card = card_service.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found",
        )

    # Get the list and board
    list_obj = db.query(List).filter(List.id == card.list_id).first()
    if not list_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found",
        )

    board = db.query(Board).filter(Board.id == list_obj.board_id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    if board.owner_id != user_id and not board.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this board",
        )

    return card


@router.get("/boards/{board_id}/labels", response_model=list[LabelResponse])
def get_board_labels(
    board_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> list[LabelResponse]:
    """Get all labels for a board."""
    _verify_board_access(db, board_id, current_user.id)

    labels = label_service.get_labels_for_board(db, board_id)

    return [
        LabelResponse.model_validate(label) for label in labels
    ]


@router.post("/boards/{board_id}/labels", response_model=LabelResponse, status_code=status.HTTP_201_CREATED)
def create_label(
    board_id: uuid.UUID,
    label_data: LabelCreate,
    db: DBSession,
    current_user: CurrentUser,
) -> LabelResponse:
    """Create a new label in a board."""
    board = _verify_board_access(db, board_id, current_user.id)

    # Only board owner can create labels
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only board owner can create labels",
        )

    # Override board_id to ensure it matches the URL
    label_data.board_id = board_id

    label = label_service.create_label(db, label_data)

    return LabelResponse.model_validate(label)


@router.get("/labels/{label_id}", response_model=LabelResponse)
def get_label(
    label_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> LabelResponse:
    """Get a label by ID."""
    label = label_service.get_label_by_id(db, label_id)
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found",
        )

    # Verify access to the board
    _verify_board_access(db, label.board_id, current_user.id)

    return LabelResponse.model_validate(label)


@router.put("/labels/{label_id}", response_model=LabelResponse)
def update_label(
    label_id: uuid.UUID,
    label_data: LabelUpdate,
    db: DBSession,
    current_user: CurrentUser,
) -> LabelResponse:
    """Update a label."""
    label = label_service.get_label_by_id(db, label_id)
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found",
        )

    # Verify access and ownership
    board = _verify_board_access(db, label.board_id, current_user.id)
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only board owner can update labels",
        )

    updated_label = label_service.update_label(db, label, label_data)

    return LabelResponse.model_validate(updated_label)


@router.delete("/labels/{label_id}", response_model=DeleteResponse)
def delete_label(
    label_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> DeleteResponse:
    """Delete a label."""
    label = label_service.get_label_by_id(db, label_id)
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found",
        )

    # Verify access and ownership
    board = _verify_board_access(db, label.board_id, current_user.id)
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only board owner can delete labels",
        )

    label_service.delete_label(db, label)

    return DeleteResponse(success=True, message="Label deleted successfully")


@router.post("/cards/{card_id}/labels/{label_id}", response_model=LabelResponse, status_code=status.HTTP_201_CREATED)
def add_label_to_card(
    card_id: uuid.UUID,
    label_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> LabelResponse:
    """Add a label to a card."""
    card = _verify_card_access(db, card_id, current_user.id)

    label = label_service.get_label_by_id(db, label_id)
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found",
        )

    # Verify label belongs to the same board
    list_obj = db.query(List).filter(List.id == card.list_id).first()
    if label.board_id != list_obj.board_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Label does not belong to the same board as the card",
        )

    label_service.add_label_to_card(db, card, label)

    return LabelResponse.model_validate(label)


@router.delete("/cards/{card_id}/labels/{label_id}", response_model=DeleteResponse)
def remove_label_from_card(
    card_id: uuid.UUID,
    label_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> DeleteResponse:
    """Remove a label from a card."""
    card = _verify_card_access(db, card_id, current_user.id)

    label = label_service.get_label_by_id(db, label_id)
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found",
        )

    removed = label_service.remove_label_from_card(db, card, label)

    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not associated with this card",
        )

    return DeleteResponse(success=True, message="Label removed from card successfully")


@router.get("/cards/{card_id}/labels", response_model=list[LabelResponse])
def get_card_labels(
    card_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> list[LabelResponse]:
    """Get all labels for a card."""
    _verify_card_access(db, card_id, current_user.id)

    labels = label_service.get_labels_for_card(db, card_id)

    return [
        LabelResponse.model_validate(label) for label in labels
    ]

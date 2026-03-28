"""Card API endpoints."""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import DBSession, CurrentUser
from app.models.card import Card
from app.models.list import List
from app.models.user import User
from app.models.board import Board
from app.schemas.card import (
    CardCreate,
    CardUpdate,
    CardMove,
    CardAssign,
    CardSearch,
    CardResponse,
    CardWithDetails,
)
from app.schemas.label import LabelResponse
from app.schemas.user import UserResponse
from app.schemas.common import DeleteResponse
from app.services import card_service
from app.services import label_service

router = APIRouter()


def _verify_card_access(
    db: Session, card_id: uuid.UUID | str, user: User
) -> tuple[Card, Board]:
    """Verify user has access to the card's board.

    Args:
        db: Database session
        card_id: Card ID to verify
        user: Current user

    Returns:
        Tuple of (card, board)

    Raises:
        HTTPException: If card not found or user doesn't have access
    """
    # Convert UUID to string for database compatibility
    card_id_str = str(card_id) if isinstance(card_id, uuid.UUID) else card_id

    card = card_service.get_card_by_id(db, card_id_str)
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

    # Check access (owner or public board)
    if board.owner_id != user.id and not board.is_public:
        # TODO: Check board members when member system is implemented
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this board",
        )

    return card, board


def _verify_list_access(
    db: Session, list_id: uuid.UUID | str, user: User
) -> List:
    """Verify user has access to the list's board.

    Args:
        db: Database session
        list_id: List ID to verify
        user: Current user

    Returns:
        The list object

    Raises:
        HTTPException: If list not found or user doesn't have access
    """
    # Convert UUID to string for database comparison
    list_id_str = str(list_id) if isinstance(list_id, uuid.UUID) else list_id

    list_obj = db.query(List).filter(List.id == list_id_str).first()
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

    # Check access
    if board.owner_id != user.id and not board.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this board",
        )

    return list_obj


def _populate_card_details(db: Session, card: Card) -> dict:
    """Populate card with labels, comments count, assignee, and related objects.

    Args:
        db: Database session
        card: Card to populate

    Returns:
        Dictionary with card details
    """
    labels = label_service.get_labels_for_card(db, card.id)
    comments_count = card_service.get_card_comments_count(db, card.id)

    # Get list and board information
    lst = db.query(List).filter(List.id == card.list_id).first()
    board = None
    if lst:
        board = db.query(Board).filter(Board.id == lst.board_id).first()

    # Build data dictionary manually to avoid type issues
    data = {
        "id": card.id,
        "list_id": card.list_id,
        "title": card.title,
        "description": card.description,
        "position": card.position,
        "priority": card.priority,
        "due_date": card.due_date.isoformat() if card.due_date else None,
        "assignee_id": card.assignee_id,
        "is_completed": card.is_completed,
        "completed_at": card.completed_at.isoformat() if card.completed_at else None,
        "attachment_count": card.attachment_count,
        "created_at": card.created_at.isoformat(),
        "updated_at": card.updated_at.isoformat(),
        "labels": [
            {"id": label.id, "name": label.name, "color": label.color} for label in labels
        ],
        "comments_count": comments_count,
        "assignee": None,
        "list": {"id": lst.id, "title": lst.title} if lst else None,
        "board": {"id": board.id, "title": board.title} if board else None,
    }

    if card.assignee_id:
        assignee = (
            db.query(User)
            .filter(User.id == card.assignee_id)
            .first()
        )
        if assignee:
            data["assignee"] = {
                "id": assignee.id,
                "username": assignee.username,
                "full_name": assignee.full_name,
                "avatar_url": assignee.avatar_url,
            }

    return data


@router.get("/{card_id}", response_model=CardWithDetails)
def get_card(
    card_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> CardWithDetails:
    """Get a card by ID with full details."""
    card, _ = _verify_card_access(db, card_id, current_user)

    return CardWithDetails(**_populate_card_details(db, card))


@router.post("/lists/{list_id}/cards", response_model=CardWithDetails, status_code=status.HTTP_201_CREATED)
def create_card(
    list_id: uuid.UUID,
    card_data: CardCreate,
    db: DBSession,
    current_user: CurrentUser,
) -> CardWithDetails:
    """Create a new card in a list."""
    list_obj = _verify_list_access(db, list_id, current_user)

    # Override list_id to ensure it matches the URL
    card_data.list_id = list_id

    card = card_service.create_card(db, card_data)

    return CardWithDetails(**_populate_card_details(db, card))


@router.put("/{card_id}", response_model=CardWithDetails)
def update_card(
    card_id: uuid.UUID,
    card_data: CardUpdate,
    db: DBSession,
    current_user: CurrentUser,
) -> CardWithDetails:
    """Update a card."""
    card, _ = _verify_card_access(db, card_id, current_user)

    # If moving to a different list, verify access
    if card_data.list_id and card_data.list_id != card.list_id:
        _verify_list_access(db, card_data.list_id, current_user)

    updated_card = card_service.update_card(db, card, card_data)

    return CardWithDetails(**_populate_card_details(db, updated_card))


@router.delete("/{card_id}", response_model=DeleteResponse)
def delete_card(
    card_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> DeleteResponse:
    """Delete a card."""
    card, _ = _verify_card_access(db, card_id, current_user)

    card_service.delete_card(db, card)

    return DeleteResponse(success=True, message="Card deleted successfully")


@router.patch("/{card_id}/move", response_model=CardWithDetails)
def move_card(
    card_id: uuid.UUID,
    move_data: CardMove,
    db: DBSession,
    current_user: CurrentUser,
) -> CardWithDetails:
    """Move a card to a different list and/or position."""
    card, _ = _verify_card_access(db, card_id, current_user)

    # Verify access to target list
    _verify_list_access(db, move_data.list_id, current_user)

    moved_card = card_service.move_card(db, card, move_data)

    return CardWithDetails(**_populate_card_details(db, moved_card))


@router.patch("/{card_id}/assign", response_model=CardWithDetails)
def assign_card(
    card_id: uuid.UUID,
    assign_data: CardAssign,
    db: DBSession,
    current_user: CurrentUser,
) -> CardWithDetails:
    """Assign or unassign a user from a card."""
    card, _ = _verify_card_access(db, card_id, current_user)

    # If assigning, verify the user exists
    if assign_data.assignee_id:
        assignee = db.query(User).filter(User.id == assign_data.assignee_id).first()
        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

    assigned_card = card_service.assign_card(db, card, assign_data)

    return CardWithDetails(**_populate_card_details(db, assigned_card))


@router.patch("/{card_id}/complete", response_model=CardWithDetails)
def toggle_card_completion(
    card_id: uuid.UUID,
    is_completed: bool,
    db: DBSession,
    current_user: CurrentUser,
) -> CardWithDetails:
    """Mark a card as completed or not completed."""
    card, _ = _verify_card_access(db, card_id, current_user)

    updated_card = card_service.toggle_card_completion(db, card, is_completed)

    return CardWithDetails(**_populate_card_details(db, updated_card))


@router.get("/boards/{board_id}/cards/search", response_model=list[CardWithDetails])
def search_cards(
    board_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
    query: str | None = None,
    label_ids: str | None = None,
    assignee_id: uuid.UUID | None = None,
    priority: str | None = None,
    is_completed: bool | None = None,
    due_date_from: str | None = None,
    due_date_to: str | None = None,
) -> list[CardWithDetails]:
    """Search cards within a board.

    Query parameters:
    - query: Search in title and description
    - label_ids: Comma-separated list of label IDs
    - assignee_id: Filter by assigned user
    - priority: Filter by priority (low, medium, high, critical)
    - is_completed: Filter by completion status
    - due_date_from: Filter by due date (from)
    - due_date_to: Filter by due date (to)
    """
    # Verify board access
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    if board.owner_id != current_user.id and not board.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this board",
        )

    # Parse label_ids if provided
    parsed_label_ids = None
    if label_ids:
        try:
            parsed_label_ids = [uuid.UUID(lid.strip()) for lid in label_ids.split(",")]
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid label_ids format",
            )

    # Parse dates if provided
    from datetime import datetime

    parsed_due_date_from = None
    parsed_due_date_to = None
    if due_date_from:
        try:
            parsed_due_date_from = datetime.fromisoformat(due_date_from.replace("Z", "+00:00"))
        except ValueError:
            pass  # Invalid date will be ignored
    if due_date_to:
        try:
            parsed_due_date_to = datetime.fromisoformat(due_date_to.replace("Z", "+00:00"))
        except ValueError:
            pass  # Invalid date will be ignored

    search_data = CardSearch(
        query=query,
        label_ids=parsed_label_ids,
        assignee_id=assignee_id,
        priority=priority,  # type: ignore
        is_completed=is_completed,
        due_date_from=parsed_due_date_from,
        due_date_to=parsed_due_date_to,
    )

    cards = card_service.search_cards(db, board_id, search_data)

    return [
        CardWithDetails(**_populate_card_details(db, card)) for card in cards
    ]


@router.get("/lists/{list_id}/cards", response_model=list[CardWithDetails])
def get_list_cards(
    list_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> list[CardWithDetails]:
    """Get all cards for a list."""
    _verify_list_access(db, list_id, current_user)

    cards = card_service.get_cards_for_list(db, list_id)

    return [
        CardWithDetails(**_populate_card_details(db, card)) for card in cards
    ]

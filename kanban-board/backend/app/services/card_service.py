"""Card service layer for business logic."""
import uuid
from datetime import datetime
from typing import Literal
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.card import Card
from app.models.list import List
from app.models.label import Label
from app.models.card_label import CardLabel
from app.models.comment import Comment
from app.schemas.card import CardCreate, CardUpdate, CardMove, CardAssign, CardSearch


def get_card_by_id(db: Session, card_id: uuid.UUID | str) -> Card | None:
    """Get a card by ID."""
    card_id_str = str(card_id) if isinstance(card_id, uuid.UUID) else card_id
    return db.query(Card).filter(Card.id == card_id_str).first()


def get_cards_for_list(db: Session, list_id: uuid.UUID | str) -> list[Card]:
    """Get all cards for a specific list, ordered by position."""
    list_id_str = str(list_id) if isinstance(list_id, uuid.UUID) else list_id
    return (
        db.query(Card)
        .filter(Card.list_id == list_id_str)
        .order_by(Card.position)
        .all()
    )


def get_cards_for_board(db: Session, board_id: uuid.UUID | str) -> list[Card]:
    """Get all cards for a specific board."""
    board_id_str = str(board_id) if isinstance(board_id, uuid.UUID) else board_id
    return (
        db.query(Card)
        .join(List, Card.list_id == List.id)
        .filter(List.board_id == board_id_str)
        .order_by(List.position, Card.position)
        .all()
    )


def create_card(db: Session, card_data: CardCreate) -> Card:
    """Create a new card.

    Args:
        db: Database session
        card_data: Card creation data

    Returns:
        Created card
    """
    # Convert UUID to string for SQLite compatibility
    list_id_str = str(card_data.list_id)
    assignee_id_str = str(card_data.assignee_id) if card_data.assignee_id else None

    # Get the max position in the list
    max_position = (
        db.query(Card.position)
        .filter(Card.list_id == list_id_str)
        .order_by(Card.position.desc())
        .first()
    )

    position = 0
    if max_position:
        position = max_position[0] + 1

    card = Card(
        list_id=list_id_str,
        title=card_data.title,
        description=card_data.description,
        position=position,
        assignee_id=assignee_id_str,
        priority=card_data.priority,
        due_date=card_data.due_date,
    )

    db.add(card)
    db.commit()
    db.refresh(card)

    return card


def update_card(db: Session, card: Card, card_data: CardUpdate) -> Card:
    """Update a card.

    Args:
        db: Database session
        card: Card to update
        card_data: Update data

    Returns:
        Updated card
    """
    update_data = card_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(card, field, value)

    db.commit()
    db.refresh(card)

    return card


def delete_card(db: Session, card: Card) -> None:
    """Delete a card.

    Args:
        db: Database session
        card: Card to delete
    """
    db.delete(card)
    db.commit()


def move_card(db: Session, card: Card, move_data: CardMove) -> Card:
    """Move a card to a different list and/or position.

    Args:
        db: Database session
        card: Card to move
        move_data: Move data (list_id and position)

    Returns:
        Moved card
    """
    old_list_id = card.list_id
    new_list_id = move_data.list_id
    new_position = move_data.position

    # If moving to a different list
    if old_list_id != new_list_id:
        # Update positions in old list (close the gap)
        db.query(Card).filter(
            and_(
                Card.list_id == old_list_id,
                Card.position > card.position,
            )
        ).update({Card.position: Card.position - 1})

        # Update positions in new list (make room)
        db.query(Card).filter(
            and_(
                Card.list_id == new_list_id,
                Card.position >= new_position,
            )
        ).update({Card.position: Card.position + 1})

        card.list_id = new_list_id
    else:
        # Moving within the same list
        if new_position > card.position:
            # Moving down: shift cards between old and new position up
            db.query(Card).filter(
                and_(
                    Card.list_id == new_list_id,
                    Card.position > card.position,
                    Card.position <= new_position,
                )
            ).update({Card.position: Card.position - 1})
        elif new_position < card.position:
            # Moving up: shift cards between new and old position down
            db.query(Card).filter(
                and_(
                    Card.list_id == new_list_id,
                    Card.position >= new_position,
                    Card.position < card.position,
                )
            ).update({Card.position: Card.position + 1})

    card.position = new_position

    db.commit()
    db.refresh(card)

    return card


def assign_card(db: Session, card: Card, assign_data: CardAssign) -> Card:
    """Assign or unassign a user from a card.

    Args:
        db: Database session
        card: Card to assign
        assign_data: Assign data (assignee_id or None to unassign)

    Returns:
        Updated card
    """
    card.assignee_id = assign_data.assignee_id

    db.commit()
    db.refresh(card)

    return card


def toggle_card_completion(
    db: Session, card: Card, is_completed: bool
) -> Card:
    """Toggle card completion status.

    Args:
        db: Database session
        card: Card to update
        is_completed: New completion status

    Returns:
        Updated card
    """
    if is_completed:
        card.mark_completed()
    else:
        card.mark_incomplete()

    db.commit()
    db.refresh(card)

    return card


def search_cards(
    db: Session,
    board_id: uuid.UUID,
    search_data: CardSearch,
) -> list[Card]:
    """Search cards within a board.

    Args:
        db: Database session
        board_id: Board ID to search in
        search_data: Search criteria

    Returns:
        List of matching cards
    """
    # Start with cards from the board
    query = (
        db.query(Card)
        .join(List, Card.list_id == List.id)
        .filter(List.board_id == board_id)
    )

    # Text search in title and description
    if search_data.query:
        query = query.filter(
            or_(
                Card.title.ilike(f"%{search_data.query}%"),
                Card.description.ilike(f"%{search_data.query}%"),
            )
        )

    # Filter by labels (if any specified)
    if search_data.label_ids:
        query = query.join(Card.labels).filter(
            CardLabel.label_id.in_(search_data.label_ids)
        )

    # Filter by assignee
    if search_data.assignee_id is not None:
        query = query.filter(Card.assignee_id == search_data.assignee_id)

    # Filter by priority
    if search_data.priority:
        query = query.filter(Card.priority == search_data.priority)

    # Filter by completion status
    if search_data.is_completed is not None:
        query = query.filter(Card.is_completed == search_data.is_completed)

    # Filter by due date range
    if search_data.due_date_from:
        query = query.filter(Card.due_date >= search_data.due_date_from)

    if search_data.due_date_to:
        query = query.filter(Card.due_date <= search_data.due_date_to)

    return query.order_by(Card.position).all()


def get_card_with_details(db: Session, card_id: uuid.UUID) -> Card | None:
    """Get a card with its related details (labels, comments, assignee)."""
    return (
        db.query(Card)
        .filter(Card.id == card_id)
        .first()
    )


def get_card_labels(db: Session, card: Card) -> list[Label]:
    """Get all labels for a card."""
    return (
        db.query(Label)
        .join(CardLabel, CardLabel.label_id == Label.id)
        .filter(CardLabel.card_id == card.id)
        .all()
    )


def get_card_comments_count(db: Session, card_id: uuid.UUID) -> int:
    """Get the count of comments for a card."""
    return (
        db.query(Comment)
        .filter(Comment.card_id == card_id)
        .count()
    )


def rebuild_list_positions(db: Session, list_id: uuid.UUID) -> None:
    """Rebuild positions for all cards in a list.

    This is useful for maintaining consistent positions after
    bulk operations or deletions.

    Args:
        db: Database session
        list_id: List ID to rebuild positions for
    """
    cards = (
        db.query(Card)
        .filter(Card.list_id == list_id)
        .order_by(Card.position)
        .all()
    )

    for index, card in enumerate(cards):
        card.position = index

    db.commit()

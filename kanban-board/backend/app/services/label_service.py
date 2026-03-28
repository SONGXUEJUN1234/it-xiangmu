"""Label service layer for business logic."""
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.label import Label
from app.models.card_label import CardLabel
from app.models.card import Card
from app.schemas.label import LabelCreate, LabelUpdate


def get_label_by_id(db: Session, label_id: uuid.UUID) -> Label | None:
    """Get a label by ID."""
    return db.query(Label).filter(Label.id == label_id).first()


def get_labels_for_board(db: Session, board_id: uuid.UUID) -> list[Label]:
    """Get all labels for a specific board."""
    return (
        db.query(Label)
        .filter(Label.board_id == board_id)
        .order_by(Label.name)
        .all()
    )


def create_label(db: Session, label_data: LabelCreate) -> Label:
    """Create a new label.

    Args:
        db: Database session
        label_data: Label creation data

    Returns:
        Created label
    """
    label = Label(
        board_id=label_data.board_id,
        name=label_data.name,
        color=label_data.color,
    )

    db.add(label)
    db.commit()
    db.refresh(label)

    return label


def update_label(db: Session, label: Label, label_data: LabelUpdate) -> Label:
    """Update a label.

    Args:
        db: Database session
        label: Label to update
        label_data: Update data

    Returns:
        Updated label
    """
    update_data = label_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(label, field, value)

    db.commit()
    db.refresh(label)

    return label


def delete_label(db: Session, label: Label) -> None:
    """Delete a label.

    Args:
        db: Database session
        label: Label to delete
    """
    db.delete(label)
    db.commit()


def add_label_to_card(
    db: Session, card: Card, label: Label
) -> CardLabel:
    """Add a label to a card.

    Args:
        db: Database session
        card: Card to add label to
        label: Label to add

    Returns:
        Created CardLabel association
    """
    # Check if association already exists
    existing = (
        db.query(CardLabel)
        .filter(
            and_(
                CardLabel.card_id == card.id,
                CardLabel.label_id == label.id,
            )
        )
        .first()
    )

    if existing:
        return existing

    card_label = CardLabel(card_id=card.id, label_id=label.id)

    db.add(card_label)
    db.commit()
    db.refresh(card_label)

    return card_label


def remove_label_from_card(
    db: Session, card: Card, label: Label
) -> bool:
    """Remove a label from a card.

    Args:
        db: Database session
        card: Card to remove label from
        label: Label to remove

    Returns:
        True if removed, False if not found
    """
    card_label = (
        db.query(CardLabel)
        .filter(
            and_(
                CardLabel.card_id == card.id,
                CardLabel.label_id == label.id,
            )
        )
        .first()
    )

    if not card_label:
        return False

    db.delete(card_label)
    db.commit()

    return True


def get_labels_for_card(db: Session, card_id: uuid.UUID) -> list[Label]:
    """Get all labels for a specific card.

    Args:
        db: Database session
        card_id: Card ID

    Returns:
        List of labels
    """
    return (
        db.query(Label)
        .join(CardLabel, CardLabel.label_id == Label.id)
        .filter(CardLabel.card_id == card_id)
        .order_by(Label.name)
        .all()
    )


def set_card_labels(
    db: Session, card: Card, label_ids: list[uuid.UUID]
) -> list[Label]:
    """Set all labels for a card (replace existing).

    Args:
        db: Database session
        card: Card to update labels for
        label_ids: List of label IDs to set

    Returns:
        List of labels
    """
    # Remove all existing labels
    db.query(CardLabel).filter(CardLabel.card_id == card.id).delete()

    # Add new labels
    for label_id in label_ids:
        card_label = CardLabel(card_id=card.id, label_id=label_id)
        db.add(card_label)

    db.commit()

    return get_labels_for_card(db, card.id)


def get_cards_with_label(
    db: Session, label_id: uuid.UUID
) -> list[Card]:
    """Get all cards that have a specific label.

    Args:
        db: Database session
        label_id: Label ID

    Returns:
        List of cards
    """
    return (
        db.query(Card)
        .join(CardLabel, CardLabel.card_id == Card.id)
        .filter(CardLabel.label_id == label_id)
        .order_by(Card.position)
        .all()
    )

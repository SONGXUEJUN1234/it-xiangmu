"""Card-Label association ORM model."""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.card import Card
    from app.models.label import Label


class CardLabel(Base):
    """Association table for many-to-many relationship between Cards and Labels."""

    __tablename__ = "card_labels"

    card_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("cards.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    label_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("labels.id", ondelete="CASCADE"), primary_key=True, index=True
    )

    # Relationships
    card: Mapped["Card"] = relationship("Card", back_populates="labels")
    label: Mapped["Label"] = relationship("Label", back_populates="card_labels")

    def __repr__(self) -> str:
        return f"<CardLabel(card_id={self.card_id}, label_id={self.label_id})>"

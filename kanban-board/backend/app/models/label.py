"""Label ORM model."""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.board import Board
    from app.models.card_label import CardLabel


class Label(UUIDMixin, TimestampMixin):
    """Label model for categorizing cards."""

    __tablename__ = "labels"

    board_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("boards.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(7), nullable=False)  # Hex color

    # Relationships
    board: Mapped["Board"] = relationship("Board", back_populates="labels")
    card_labels: Mapped[list["CardLabel"]] = relationship(
        "CardLabel", back_populates="label", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Label(id={self.id}, name={self.name}, color={self.color})>"

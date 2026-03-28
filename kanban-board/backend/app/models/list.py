"""List ORM model."""
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.board import Board
    from app.models.card import Card


class List(UUIDMixin, TimestampMixin):
    """List model representing columns in a kanban board."""

    __tablename__ = "lists"

    board_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("boards.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    board: Mapped["Board"] = relationship("Board", back_populates="lists")
    cards: Mapped[list["Card"]] = relationship(
        "Card", back_populates="list", cascade="all, delete-orphan", order_by="Card.position"
    )

    def __repr__(self) -> str:
        return f"<List(id={self.id}, title={self.title}, position={self.position})>"

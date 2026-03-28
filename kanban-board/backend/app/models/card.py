"""Card ORM model."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.list import List
    from app.models.user import User
    from app.models.comment import Comment
    from app.models.card_label import CardLabel


class Card(UUIDMixin, TimestampMixin):
    """Card model representing tasks in a kanban board."""

    __tablename__ = "cards"

    list_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("lists.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    assignee_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    priority: Mapped[str] = mapped_column(String(10), default="medium", nullable=False)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    attachment_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    list: Mapped["List"] = relationship("List", back_populates="cards")
    assignee: Mapped["User | None"] = relationship("User", back_populates="assigned_cards", foreign_keys=[assignee_id])
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="card", cascade="all, delete-orphan"
    )
    labels: Mapped[list["CardLabel"]] = relationship(
        "CardLabel", back_populates="card", cascade="all, delete-orphan"
    )

    def mark_completed(self) -> None:
        """Mark the card as completed."""
        self.is_completed = True
        self.completed_at = datetime.now(timezone.utc)

    def mark_incomplete(self) -> None:
        """Mark the card as incomplete."""
        self.is_completed = False
        self.completed_at = None

    def __repr__(self) -> str:
        return f"<Card(id={self.id}, title={self.title}, position={self.position})>"

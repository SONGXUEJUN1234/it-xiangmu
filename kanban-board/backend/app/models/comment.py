"""Comment ORM model."""
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.card import Card
    from app.models.user import User


class Comment(UUIDMixin, TimestampMixin):
    """Comment model for user discussions on cards."""

    __tablename__ = "comments"

    card_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    parent_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("comments.id", ondelete="CASCADE")
    )
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    card: Mapped["Card"] = relationship("Card", back_populates="comments")
    author: Mapped["User"] = relationship("User", back_populates="comments")

    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, card_id={self.card_id}, user_id={self.user_id})>"

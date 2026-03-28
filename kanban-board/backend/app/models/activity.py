"""Activity ORM model."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, String, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import UUIDMixin

if TYPE_CHECKING:
    from app.models.board import Board
    from app.models.user import User


class Activity(UUIDMixin):
    """Activity model for tracking all actions within a board."""

    __tablename__ = "activities"

    board_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("boards.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    action: Mapped[str] = mapped_column(String(50), nullable=False)  # created/updated/deleted/moved/etc
    entity_type: Mapped[str] = mapped_column(String(20), nullable=False)  # board/list/card/member/label/comment
    entity_id: Mapped[str] = mapped_column(nullable=False)
    entity_title: Mapped[str | None] = mapped_column(String(200))
    changes: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    board: Mapped["Board"] = relationship("Board", back_populates="activities")
    user: Mapped["User"] = relationship("User")

    def __repr__(self) -> str:
        return f"<Activity(id={self.id}, action={self.action}, entity_type={self.entity_type})>"

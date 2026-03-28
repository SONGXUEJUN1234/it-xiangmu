"""Board Member ORM model."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import UUIDMixin

if TYPE_CHECKING:
    from app.models.board import Board
    from app.models.user import User


class BoardMember(UUIDMixin):
    """Board member model for user-board relationships with roles."""

    __tablename__ = "board_members"

    board_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("boards.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # owner/admin/member/viewer
    joined_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    board: Mapped["Board"] = relationship("Board", back_populates="members")
    user: Mapped["User"] = relationship("User")

    def __repr__(self) -> str:
        return f"<BoardMember(board_id={self.board_id}, user_id={self.user_id}, role={self.role})>"

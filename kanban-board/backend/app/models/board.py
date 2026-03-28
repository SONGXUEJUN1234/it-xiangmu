"""Board ORM model."""
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Text, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.list import List
    from app.models.label import Label
    from app.models.activity import Activity
    from app.models.board_member import BoardMember


class Board(UUIDMixin, TimestampMixin):
    """Board model representing kanban boards."""

    __tablename__ = "boards"

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    owner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    background_url: Mapped[str | None] = mapped_column(String(500))
    background_color: Mapped[str | None] = mapped_column(String(7))  # Hex color
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="boards")
    lists: Mapped[list["List"]] = relationship(
        "List", back_populates="board", cascade="all, delete-orphan", order_by="List.position"
    )
    labels: Mapped[list["Label"]] = relationship(
        "Label", back_populates="board", cascade="all, delete-orphan"
    )
    activities: Mapped[list["Activity"]] = relationship(
        "Activity", back_populates="board", cascade="all, delete-orphan"
    )
    members: Mapped[list["BoardMember"]] = relationship(
        "BoardMember", back_populates="board", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Board(id={self.id}, title={self.title}, owner_id={self.owner_id})>"

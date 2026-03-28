"""Comment-related Pydantic schemas."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class CommentBase(BaseModel):
    """Base comment schema."""

    content: str = Field(min_length=1, max_length=5000)
    parent_id: uuid.UUID | None = None


class CommentCreate(CommentBase):
    """Schema for creating a comment."""

    card_id: uuid.UUID


class CommentUpdate(BaseModel):
    """Schema for updating a comment."""

    content: str = Field(min_length=1, max_length=5000)


class CommentResponse(CommentBase):
    """Schema for comment response."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    card_id: uuid.UUID
    user_id: uuid.UUID
    is_edited: bool
    created_at: datetime
    updated_at: datetime


class CommentWithAuthor(CommentResponse):
    """Schema for comment response with author."""

    author: "UserResponse"


# Import at the end to avoid circular imports
from app.schemas.user import UserResponse  # noqa: E402

CommentWithAuthor.model_rebuild()

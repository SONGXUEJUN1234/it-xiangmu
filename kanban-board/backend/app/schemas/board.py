"""Board-related Pydantic schemas."""
import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class BoardBase(BaseModel):
    """Base board schema."""

    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    background_color: str | None = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    background_url: str | None = Field(None, max_length=500)
    is_public: bool = False


class BoardCreate(BoardBase):
    """Schema for creating a board."""

    pass


class BoardUpdate(BoardBase):
    """Schema for updating a board."""

    title: str | None = Field(None, min_length=1, max_length=100)
    is_archived: bool | None = None


class BoardMemberRole(BaseModel):
    """Schema for board member role."""

    user_id: uuid.UUID
    role: Literal["owner", "admin", "member", "viewer"]


class BoardResponse(BoardBase):
    """Schema for board response."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    owner_id: uuid.UUID
    is_archived: bool
    created_at: datetime
    updated_at: datetime


class BoardWithMembers(BoardResponse):
    """Schema for board response with members."""

    members_count: int
    lists_count: int
    cards_count: int
    lists: list[dict] = []

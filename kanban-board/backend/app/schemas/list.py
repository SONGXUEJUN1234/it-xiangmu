"""List-related Pydantic schemas."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ListBase(BaseModel):
    """Base list schema."""

    title: str = Field(min_length=1, max_length=100)
    position: int = Field(ge=0)


class ListCreate(ListBase):
    """Schema for creating a list."""

    board_id: uuid.UUID


class ListUpdate(BaseModel):
    """Schema for updating a list."""

    title: str | None = Field(None, min_length=1, max_length=100)
    position: int | None = Field(None, ge=0)
    is_archived: bool | None = None


class ListResponse(ListBase):
    """Schema for list response."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    board_id: uuid.UUID
    is_archived: bool
    created_at: datetime
    updated_at: datetime


class ListWithCards(ListResponse):
    """Schema for list response with cards."""

    cards_count: int

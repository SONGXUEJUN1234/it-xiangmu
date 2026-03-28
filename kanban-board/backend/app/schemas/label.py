"""Label-related Pydantic schemas."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class LabelBase(BaseModel):
    """Base label schema."""

    name: str = Field(min_length=1, max_length=50)
    color: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$")  # Hex color


class LabelCreate(LabelBase):
    """Schema for creating a label."""

    board_id: uuid.UUID


class LabelUpdate(BaseModel):
    """Schema for updating a label."""

    name: str | None = Field(None, min_length=1, max_length=50)
    color: str | None = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")


class LabelResponse(LabelBase):
    """Schema for label response."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    board_id: uuid.UUID
    created_at: datetime

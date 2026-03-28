"""Card-related Pydantic schemas."""
import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class CardBase(BaseModel):
    """Base card schema."""

    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    position: int = Field(ge=0)
    priority: Literal["low", "medium", "high", "critical"] = "medium"
    due_date: datetime | None = None


class CardCreate(BaseModel):
    """Schema for creating a card."""

    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    position: int | None = Field(None, ge=0)
    priority: Literal["low", "medium", "high", "critical"] = "medium"
    due_date: datetime | None = None
    list_id: uuid.UUID
    assignee_id: uuid.UUID | None = None


class CardUpdate(BaseModel):
    """Schema for updating a card."""

    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    list_id: uuid.UUID | None = None
    position: int | None = Field(None, ge=0)
    assignee_id: uuid.UUID | None = None
    priority: Literal["low", "medium", "high", "critical"] | None = None
    due_date: datetime | None = None
    is_completed: bool | None = None


class CardMove(BaseModel):
    """Schema for moving a card."""

    list_id: uuid.UUID
    position: int = Field(ge=0)


class CardAssign(BaseModel):
    """Schema for assigning a user to a card."""

    assignee_id: uuid.UUID | None = None  # None to unassign


class CardSearch(BaseModel):
    """Schema for searching cards."""

    query: str | None = None
    label_ids: list[uuid.UUID] | None = None
    assignee_id: uuid.UUID | None = None
    priority: Literal["low", "medium", "high", "critical"] | None = None
    is_completed: bool | None = None
    due_date_from: datetime | None = None
    due_date_to: datetime | None = None


class CardResponse(CardBase):
    """Schema for card response."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    list_id: uuid.UUID
    assignee_id: uuid.UUID | None
    is_completed: bool
    completed_at: datetime | None
    attachment_count: int
    created_at: datetime
    updated_at: datetime


class CardWithDetails(CardResponse):
    """Schema for card response with details."""

    labels: list["LabelResponse"] = []
    comments_count: int
    assignee: "UserResponse | None" = None
    list: "dict | None" = None
    board: "dict | None" = None


# Prevents circular imports
from app.schemas.label import LabelResponse
from app.schemas.user import UserResponse

CardWithDetails.model_rebuild()

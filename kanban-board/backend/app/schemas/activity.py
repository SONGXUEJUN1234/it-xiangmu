"""Activity-related Pydantic schemas."""
import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, ConfigDict


class ActivityBase(BaseModel):
    """Base activity schema."""

    action: str = Field(description="Action performed (created/updated/deleted/moved/etc)")
    entity_type: str = Field(description="Type of entity (board/list/card/member/label/comment)")
    entity_id: uuid.UUID
    entity_title: str | None = Field(None, max_length=200)


class ActivityCreate(ActivityBase):
    """Schema for creating an activity."""

    board_id: uuid.UUID
    user_id: uuid.UUID
    changes: dict[str, Any] | None = None


class ActivityUpdate(BaseModel):
    """Schema for updating an activity (limited use)."""

    entity_title: str | None = Field(None, max_length=200)
    changes: dict[str, Any] | None = None


class ActivityResponse(ActivityBase):
    """Schema for activity response."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    board_id: uuid.UUID
    user_id: uuid.UUID
    changes: dict[str, Any] | None
    created_at: datetime


class ActivityWithUser(ActivityResponse):
    """Schema for activity response with user."""

    user: "UserResponse"


# Import at the end to avoid circular imports
from app.schemas.user import UserResponse  # noqa: E402

ActivityWithUser.model_rebuild()

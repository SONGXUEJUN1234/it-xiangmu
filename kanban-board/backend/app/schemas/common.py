"""Common response schemas for API responses."""
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    """Standard API response wrapper."""

    success: bool = True
    data: T
    message: str | None = None


class ErrorDetail(BaseModel):
    """Error detail for validation errors."""

    field: str | None = None
    message: str


class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = False
    error: ErrorDetail | None = None
    message: str
    details: dict[str, Any] | None = None


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    page: int = Field(ge=1, description="Current page number")
    page_size: int = Field(ge=1, le=100, description="Number of items per page")
    total: int = Field(ge=0, description="Total number of items")
    total_pages: int = Field(ge=0, description="Total number of pages")

    @classmethod
    def create(cls, page: int, page_size: int, total: int) -> "PaginationMeta":
        """Create pagination metadata from total count."""
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
        return cls(page=page, page_size=page_size, total=total, total_pages=total_pages)


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated API response."""

    success: bool = True
    data: list[T]
    pagination: PaginationMeta


# Common request/response models
class IDResponse(BaseModel):
    """Response with just an ID."""

    id: str


class MessageResponse(BaseModel):
    """Simple message response."""

    message: str


class DeleteResponse(BaseModel):
    """Response for delete operations."""

    success: bool = True
    message: str = "Resource deleted successfully"

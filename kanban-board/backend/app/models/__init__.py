"""Import all models for Alembic autogenerate support."""
from app.models.activity import Activity
from app.models.base import Base
from app.models.board import Board
from app.models.board_member import BoardMember
from app.models.card import Card
from app.models.card_label import CardLabel
from app.models.comment import Comment
from app.models.label import Label
from app.models.list import List
from app.models.refresh_token import RefreshToken
from app.models.user import User

__all__ = [
    "Activity",
    "Base",
    "Board",
    "BoardMember",
    "Card",
    "CardLabel",
    "Comment",
    "Label",
    "List",
    "RefreshToken",
    "User",
]

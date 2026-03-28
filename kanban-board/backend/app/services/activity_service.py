"""Activity service for tracking and managing board activities."""
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy import desc, or_

from app.models.activity import Activity
from app.models.board import Board
from app.models.user import User
from app.models.card import Card
from app.models.list import List as ListModel
from app.models.label import Label
from app.models.comment import Comment


class ActivityService:
    """Service for managing activity logs."""

    # Entity type constants
    ENTITY_BOARD = "board"
    ENTITY_LIST = "list"
    ENTITY_CARD = "card"
    ENTITY_MEMBER = "member"
    ENTITY_LABEL = "label"
    ENTITY_COMMENT = "comment"

    # Action constants
    ACTION_CREATED = "created"
    ACTION_UPDATED = "updated"
    ACTION_DELETED = "deleted"
    ACTION_MOVED = "moved"
    ACTION_ARCHIVED = "archived"
    ACTION_RESTORED = "restored"
    ACTION_ASSIGNED = "assigned"
    ACTION_UNASSIGNED = "unassigned"
    ACTION_COMMENTED = "commented"

    @staticmethod
    def log_activity(
        db: Session,
        board_id: uuid.UUID,
        user_id: uuid.UUID,
        action: str,
        entity_type: str,
        entity_id: uuid.UUID,
        entity_title: str | None = None,
        changes: dict[str, Any] | None = None,
    ) -> Activity:
        """
        Log a new activity.

        Args:
            db: Database session
            board_id: ID of the board where the action occurred
            user_id: ID of the user who performed the action
            action: Type of action (created/updated/deleted/moved/etc)
            entity_type: Type of entity (board/list/card/member/label/comment)
            entity_id: ID of the affected entity
            entity_title: Optional title of the entity for display
            changes: Optional dictionary of changes made

        Returns:
            The created Activity record
        """
        activity = Activity(
            board_id=board_id,
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_title=entity_title,
            changes=changes,
            created_at=datetime.now(timezone.utc),
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity

    @staticmethod
    def get_activities_for_board(
        db: Session,
        board_id: uuid.UUID,
        page: int = 1,
        page_size: int = 50,
        entity_type: str | None = None,
        user_id: uuid.UUID | None = None,
    ) -> tuple[list[Activity], int]:
        """
        Get activities for a specific board with pagination and filtering.

        Args:
            db: Database session
            board_id: ID of the board
            page: Page number (1-indexed)
            page_size: Number of items per page
            entity_type: Filter by entity type
            user_id: Filter by user who performed the action

        Returns:
            Tuple of (list of activities, total count)
        """
        query = db.query(Activity).filter(Activity.board_id == board_id)

        if entity_type:
            query = query.filter(Activity.entity_type == entity_type)

        if user_id:
            query = query.filter(Activity.user_id == user_id)

        # Get total count
        total = query.count()

        # Apply pagination and ordering
        activities = (
            query.order_by(desc(Activity.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return activities, total

    @staticmethod
    def get_activities_for_entity(
        db: Session,
        board_id: uuid.UUID,
        entity_type: str,
        entity_id: uuid.UUID,
        limit: int = 100,
    ) -> list[Activity]:
        """
        Get all activities for a specific entity.

        Args:
            db: Database session
            board_id: ID of the board
            entity_type: Type of entity
            entity_id: ID of the entity
            limit: Maximum number of activities to return

        Returns:
            List of activities for the entity
        """
        return (
            db.query(Activity)
            .filter(
                Activity.board_id == board_id,
                Activity.entity_type == entity_type,
                Activity.entity_id == entity_id,
            )
            .order_by(desc(Activity.created_at))
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_activity_by_id(db: Session, activity_id: uuid.UUID) -> Activity | None:
        """
        Get a specific activity by ID.

        Args:
            db: Database session
            activity_id: ID of the activity

        Returns:
            The Activity record if found, None otherwise
        """
        return db.query(Activity).filter(Activity.id == activity_id).first()

    @staticmethod
    def delete_old_activities(db: Session, days: int = 90) -> int:
        """
        Delete activities older than the specified number of days.

        Args:
            db: Database session
            days: Number of days to keep activities

        Returns:
            Number of activities deleted
        """
        from datetime import timedelta

        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

        deleted = (
            db.query(Activity)
            .filter(Activity.created_at < cutoff_date)
            .delete()
        )
        db.commit()
        return deleted

    @staticmethod
    def delete_activities_for_entity(
        db: Session,
        entity_type: str,
        entity_id: uuid.UUID,
    ) -> int:
        """
        Delete all activities for a specific entity.

        Args:
            db: Database session
            entity_type: Type of entity
            entity_id: ID of the entity

        Returns:
            Number of activities deleted
        """
        deleted = (
            db.query(Activity)
            .filter(
                Activity.entity_type == entity_type,
                Activity.entity_id == entity_id,
            )
            .delete()
        )
        db.commit()
        return deleted


class ActivityLogger:
    """
    Helper class for convenient activity logging.
    Provides methods to log activities for different entity types.
    """

    @staticmethod
    def _get_entity_info(entity: Board | ListModel | Card | Label | Comment) -> tuple[str, uuid.UUID, str | None]:
        """Extract entity type, id, and title from an entity."""
        if isinstance(entity, Board):
            return ActivityService.ENTITY_BOARD, entity.id, entity.title
        elif isinstance(entity, ListModel):
            return ActivityService.ENTITY_LIST, entity.id, entity.title
        elif isinstance(entity, Card):
            return ActivityService.ENTITY_CARD, entity.id, entity.title
        elif isinstance(entity, Label):
            return ActivityService.ENTITY_LABEL, entity.id, entity.name
        elif isinstance(entity, Comment):
            return ActivityService.ENTITY_COMMENT, entity.id, None
        else:
            raise ValueError(f"Unsupported entity type: {type(entity)}")

    @classmethod
    def log_created(
        cls,
        db: Session,
        entity: Board | ListModel | Card | Label | Comment,
        user_id: uuid.UUID,
        changes: dict[str, Any] | None = None,
    ) -> Activity:
        """Log entity creation."""
        entity_type, entity_id, entity_title = cls._get_entity_info(entity)
        board_id = cls._get_board_id(entity)

        return ActivityService.log_activity(
            db=db,
            board_id=board_id,
            user_id=user_id,
            action=ActivityService.ACTION_CREATED,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_title=entity_title,
            changes=changes,
        )

    @classmethod
    def log_updated(
        cls,
        db: Session,
        entity: Board | ListModel | Card | Label | Comment,
        user_id: uuid.UUID,
        changes: dict[str, Any] | None = None,
    ) -> Activity:
        """Log entity update."""
        entity_type, entity_id, entity_title = cls._get_entity_info(entity)
        board_id = cls._get_board_id(entity)

        return ActivityService.log_activity(
            db=db,
            board_id=board_id,
            user_id=user_id,
            action=ActivityService.ACTION_UPDATED,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_title=entity_title,
            changes=changes,
        )

    @classmethod
    def log_deleted(
        cls,
        db: Session,
        entity: Board | ListModel | Card | Label | Comment,
        user_id: uuid.UUID,
        changes: dict[str, Any] | None = None,
    ) -> Activity:
        """Log entity deletion."""
        entity_type, entity_id, entity_title = cls._get_entity_info(entity)
        board_id = cls._get_board_id(entity)

        return ActivityService.log_activity(
            db=db,
            board_id=board_id,
            user_id=user_id,
            action=ActivityService.ACTION_DELETED,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_title=entity_title,
            changes=changes,
        )

    @classmethod
    def log_moved(
        cls,
        db: Session,
        entity: Card | ListModel,
        user_id: uuid.UUID,
        changes: dict[str, Any] | None = None,
    ) -> Activity:
        """Log entity move (for cards between lists, or lists position change)."""
        entity_type, entity_id, entity_title = cls._get_entity_info(entity)
        board_id = cls._get_board_id(entity)

        return ActivityService.log_activity(
            db=db,
            board_id=board_id,
            user_id=user_id,
            action=ActivityService.ACTION_MOVED,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_title=entity_title,
            changes=changes,
        )

    @classmethod
    def log_commented(
        cls,
        db: Session,
        card: Card,
        comment: Comment,
        user_id: uuid.UUID,
    ) -> Activity:
        """Log a comment on a card."""
        board_id = cls._get_board_id(card)

        return ActivityService.log_activity(
            db=db,
            board_id=board_id,
            user_id=user_id,
            action=ActivityService.ACTION_COMMENTED,
            entity_type=ActivityService.ENTITY_CARD,
            entity_id=card.id,
            entity_title=card.title,
            changes={"comment_id": str(comment.id), "content_preview": comment.content[:100]},
        )

    @classmethod
    def log_assigned(
        cls,
        db: Session,
        card: Card,
        user_id: uuid.UUID,
        assigned_to_id: uuid.UUID,
    ) -> Activity:
        """Log card assignment."""
        board_id = cls._get_board_id(card)

        return ActivityService.log_activity(
            db=db,
            board_id=board_id,
            user_id=user_id,
            action=ActivityService.ACTION_ASSIGNED,
            entity_type=ActivityService.ENTITY_CARD,
            entity_id=card.id,
            entity_title=card.title,
            changes={"assigned_to": str(assigned_to_id)},
        )

    @staticmethod
    def _get_board_id(entity: Board | ListModel | Card | Label | Comment) -> uuid.UUID:
        """Get the board ID for an entity."""
        if isinstance(entity, Board):
            return entity.id
        elif isinstance(entity, ListModel):
            return entity.board_id
        elif isinstance(entity, Card):
            # Need to load the list to get board_id
            if entity.list:
                return entity.list.board_id
            # If not loaded, query for it
            from app.models.list import List as ListModelLocal
            lst = (
                entity.__class__._sa_instance_state.session.query(ListModelLocal)
                .filter(ListModelLocal.id == entity.list_id)
                .first()
            )
            return lst.board_id if lst else None
        elif isinstance(entity, Comment):
            # Need to load the card to get board_id
            if entity.card and entity.card.list:
                return entity.card.list.board_id
            return None
        elif isinstance(entity, Label):
            return entity.board_id
        return None

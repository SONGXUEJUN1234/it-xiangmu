"""Comment service for managing card comments."""
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.comment import Comment
from app.models.card import Card
from app.models.user import User
from app.services.activity_service import ActivityLogger


class CommentService:
    """Service for managing comments on cards."""

    @staticmethod
    def get_comment_by_id(db: Session, comment_id: uuid.UUID | str) -> Comment | None:
        """
        Get a specific comment by ID.

        Args:
            db: Database session
            comment_id: ID of the comment

        Returns:
            The Comment record if found, None otherwise
        """
        comment_id_str = str(comment_id) if isinstance(comment_id, uuid.UUID) else comment_id
        return db.query(Comment).filter(Comment.id == comment_id_str).first()

    @staticmethod
    def get_comments_for_card(
        db: Session,
        card_id: uuid.UUID | str,
        page: int = 1,
        page_size: int = 20,
        include_replies: bool = True,
    ) -> tuple[list[Comment], int]:
        """
        Get comments for a specific card with pagination.

        Args:
            db: Database session
            card_id: ID of the card
            page: Page number (1-indexed)
            page_size: Number of items per page
            include_replies: Whether to include replies to comments

        Returns:
            Tuple of (list of comments, total count)
        """
        card_id_str = str(card_id) if isinstance(card_id, uuid.UUID) else card_id
        query = db.query(Comment).filter(Comment.card_id == card_id_str)

        if not include_replies:
            # Only get top-level comments (no parent)
            query = query.filter(Comment.parent_id.is_(None))

        # Get total count
        total = query.count()

        # Apply pagination and ordering
        comments = (
            query.order_by(desc(Comment.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return comments, total

    @staticmethod
    def get_replies(
        db: Session,
        comment_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Comment], int]:
        """
        Get replies to a specific comment.

        Args:
            db: Database session
            comment_id: ID of the parent comment
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            Tuple of (list of replies, total count)
        """
        query = db.query(Comment).filter(Comment.parent_id == comment_id)

        # Get total count
        total = query.count()

        # Apply pagination and ordering
        replies = (
            query.order_by(Comment.created_at)  # Oldest first for replies
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return replies, total

    @staticmethod
    def create_comment(
        db: Session,
        card_id: uuid.UUID,
        user_id: uuid.UUID,
        content: str,
        parent_id: uuid.UUID | None = None,
        log_activity: bool = True,
    ) -> Comment:
        """
        Create a new comment on a card.

        Args:
            db: Database session
            card_id: ID of the card
            user_id: ID of the user creating the comment
            content: Comment content
            parent_id: Optional ID of parent comment for replies
            log_activity: Whether to log activity

        Returns:
            The created Comment record

        Raises:
            ValueError: If card doesn't exist or parent_id is invalid
        """
        # Verify card exists
        card_id_str = str(card_id) if isinstance(card_id, uuid.UUID) else card_id
        card = db.query(Card).filter(Card.id == card_id_str).first()
        if not card:
            raise ValueError(f"Card with id {card_id} not found")

        # Verify parent comment exists if provided
        if parent_id:
            parent_id_str = str(parent_id) if isinstance(parent_id, uuid.UUID) else parent_id
            parent_comment = db.query(Comment).filter(Comment.id == parent_id_str).first()
            if not parent_comment:
                raise ValueError(f"Parent comment with id {parent_id} not found")
            if str(parent_comment.card_id) != card_id_str:
                raise ValueError("Parent comment must belong to the same card")

        user_id_str = str(user_id) if isinstance(user_id, uuid.UUID) else user_id
        parent_id_str = str(parent_id) if isinstance(parent_id, uuid.UUID) else parent_id

        comment = Comment(
            card_id=card_id_str,
            user_id=user_id_str,
            content=content,
            parent_id=parent_id_str,
            is_edited=False,
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)

        # Log activity
        if log_activity:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                ActivityLogger.log_commented(db, card, comment, user_id)

        return comment

    @staticmethod
    def update_comment(
        db: Session,
        comment_id: uuid.UUID,
        user_id: uuid.UUID,
        content: str,
        log_activity: bool = False,
    ) -> Comment:
        """
        Update a comment's content.

        Args:
            db: Database session
            comment_id: ID of the comment
            user_id: ID of the user updating the comment
            content: New comment content
            log_activity: Whether to log activity

        Returns:
            The updated Comment record

        Raises:
            ValueError: If comment doesn't exist or user doesn't own it
        """
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise ValueError(f"Comment with id {comment_id} not found")

        if comment.user_id != user_id:
            raise ValueError("You can only edit your own comments")

        old_content = comment.content
        comment.content = content
        comment.is_edited = True

        db.commit()
        db.refresh(comment)

        # Log activity for comment update on the card
        if log_activity:
            from app.services.activity_service import ActivityService
            from app.models.list import List as ListModel

            # Get board_id
            if comment.card and comment.card.list:
                ActivityService.log_activity(
                    db=db,
                    board_id=comment.card.list.board_id,
                    user_id=user_id,
                    action="updated",
                    entity_type=ActivityService.ENTITY_COMMENT,
                    entity_id=comment.id,
                    entity_title=None,
                    changes={"old_content": old_content[:100], "new_content": content[:100]},
                )

        return comment

    @staticmethod
    def delete_comment(
        db: Session,
        comment_id: uuid.UUID,
        user_id: uuid.UUID,
        log_activity: bool = False,
    ) -> bool:
        """
        Delete a comment.

        Args:
            db: Database session
            comment_id: ID of the comment
            user_id: ID of the user deleting the comment
            log_activity: Whether to log activity

        Returns:
            True if comment was deleted, False otherwise

        Raises:
            ValueError: If comment doesn't exist or user doesn't own it
        """
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise ValueError(f"Comment with id {comment_id} not found")

        if comment.user_id != user_id:
            raise ValueError("You can only delete your own comments")

        # Store info for activity log before deleting
        card_id = comment.card_id

        db.delete(comment)
        db.commit()

        # Log activity
        if log_activity:
            from app.services.activity_service import ActivityService
            from app.models.card import Card
            from app.models.list import List as ListModel

            card = db.query(Card).filter(Card.id == card_id).first()
            if card and card.list:
                ActivityService.log_activity(
                    db=db,
                    board_id=card.list.board_id,
                    user_id=user_id,
                    action=ActivityService.ACTION_DELETED,
                    entity_type=ActivityService.ENTITY_COMMENT,
                    entity_id=comment_id,
                    entity_title=None,
                    changes={"content": comment.content[:100]},
                )

        return True

    @staticmethod
    def can_edit_comment(db: Session, comment_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """
        Check if a user can edit a comment.

        Args:
            db: Database session
            comment_id: ID of the comment
            user_id: ID of the user

        Returns:
            True if user can edit, False otherwise
        """
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        return comment is not None and comment.user_id == user_id

    @staticmethod
    def can_delete_comment(db: Session, comment_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """
        Check if a user can delete a comment.

        Args:
            db: Database session
            comment_id: ID of the comment
            user_id: ID of the user

        Returns:
            True if user can delete, False otherwise
        """
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        return comment is not None and comment.user_id == user_id

    @staticmethod
    def get_comment_count(db: Session, card_id: uuid.UUID) -> int:
        """
        Get the total number of comments on a card (including replies).

        Args:
            db: Database session
            card_id: ID of the card

        Returns:
            Number of comments
        """
        return db.query(Comment).filter(Comment.card_id == card_id).count()

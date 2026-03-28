"""List service layer for business logic."""
import uuid
from typing import Literal
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status

from app.models.list import List as ListModel
from app.models.card import Card
from app.schemas.list import ListCreate, ListUpdate
from app.services.board_service import check_board_access


def get_list_by_id(db: Session, list_id: uuid.UUID, user_id: uuid.UUID) -> ListModel:
    """Get a list by ID with access check.

    Args:
        db: Database session
        list_id: List ID
        user_id: User ID

    Returns:
        List object

    Raises:
        HTTPException: If list not found or access denied
    """
    lst = db.query(ListModel).filter(ListModel.id == list_id).first()

    if not lst:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found",
        )

    # Check board access
    check_board_access(db, lst.board_id, user_id)

    return lst


def get_lists_for_board(
    db: Session,
    board_id: uuid.UUID,
    user_id: uuid.UUID,
    include_archived: bool = False,
) -> list[ListModel]:
    """Get all lists for a board.

    Args:
        db: Database session
        board_id: Board ID
        user_id: User ID
        include_archived: Whether to include archived lists

    Returns:
        List of List objects ordered by position

    Raises:
        HTTPException: If access denied
    """
    # Check board access
    check_board_access(db, board_id, user_id)

    board_id_str = str(board_id)
    query = db.query(ListModel).filter(ListModel.board_id == board_id_str)

    if not include_archived:
        query = query.filter(ListModel.is_archived == False)

    return query.order_by(ListModel.position).all()


def create_list(db: Session, list_data: ListCreate, user_id: uuid.UUID) -> ListModel:
    """Create a new list.

    Args:
        db: Database session
        list_data: List creation data
        user_id: User ID creating the list

    Returns:
        Created List object

    Raises:
        HTTPException: If access denied
    """
    # Convert UUID to string for SQLite compatibility
    board_id_str = str(list_data.board_id)

    # Check board access - need member role
    check_board_access(db, board_id_str, user_id, require_role="member")

    # Get the max position for this board
    max_position = db.query(ListModel).filter(
        ListModel.board_id == board_id_str
    ).count()

    # Create list
    lst = ListModel(
        board_id=board_id_str,
        title=list_data.title,
        position=list_data.position if list_data.position is not None else max_position,
    )
    db.add(lst)
    db.commit()
    db.refresh(lst)

    # Reposition if needed
    if list_data.position is not None:
        _reposition_after_insert(db, lst)

    return lst


def update_list(
    db: Session,
    list_id: uuid.UUID,
    list_data: ListUpdate,
    user_id: uuid.UUID,
) -> ListModel:
    """Update a list.

    Args:
        db: Database session
        list_id: List ID
        list_data: List update data
        user_id: User ID of the user making the update

    Returns:
        Updated List object

    Raises:
        HTTPException: If list not found or access denied
    """
    lst = get_list_by_id(db, list_id, user_id)

    # Check board access - need member role to update
    check_board_access(db, lst.board_id, user_id, require_role="member")

    # Update fields
    update_data = list_data.model_dump(exclude_unset=True)

    old_position = lst.position
    for field, value in update_data.items():
        setattr(lst, field, value)

    db.commit()
    db.refresh(lst)

    # Reposition if position changed
    if "position" in update_data and update_data["position"] != old_position:
        _reposition_after_update(db, lst, old_position)

    return lst


def delete_list(db: Session, list_id: uuid.UUID, user_id: uuid.UUID) -> None:
    """Delete a list.

    Args:
        db: Database session
        list_id: List ID
        user_id: User ID of the user making the deletion

    Raises:
        HTTPException: If list not found or access denied
    """
    lst = get_list_by_id(db, list_id, user_id)

    # Check board access - need member role to delete
    check_board_access(db, lst.board_id, user_id, require_role="member")

    db.delete(lst)
    db.commit()


def reorder_lists(
    db: Session,
    board_id: uuid.UUID,
    list_positions: dict[uuid.UUID, int],
    user_id: uuid.UUID,
) -> list[ListModel]:
    """Reorder lists on a board.

    Args:
        db: Database session
        board_id: Board ID
        list_positions: Dictionary mapping list IDs to new positions
        user_id: User ID making the request

    Returns:
        Updated list of List objects

    Raises:
        HTTPException: If access denied or invalid data
    """
    # Check board access - need member role
    check_board_access(db, board_id, user_id, require_role="member")

    # Verify all lists belong to this board
    list_ids = list(list_positions.keys())
    lists = db.query(ListModel).filter(
        and_(
            ListModel.id.in_(list_ids),
            ListModel.board_id == board_id
        )
    ).all()

    if len(lists) != len(list_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more lists not found in this board",
        )

    # Update positions
    for lst in lists:
        lst.position = list_positions[lst.id]

    db.commit()

    # Return refreshed lists ordered by position
    return db.query(ListModel).filter(
        and_(
            ListModel.board_id == board_id,
            ListModel.is_archived == False
        )
    ).order_by(ListModel.position).all()


def get_cards_count_for_list(db: Session, list_id: uuid.UUID) -> int:
    """Get the number of cards in a list.

    Args:
        db: Database session
        list_id: List ID

    Returns:
        Number of cards in the list
    """
    return db.query(Card).filter(Card.list_id == list_id).count()


def _reposition_after_insert(db: Session, lst: ListModel) -> None:
    """Reposition lists after inserting a new list.

    Args:
        db: Database session
        lst: The newly inserted list
    """
    # Shift lists with position >= new list's position
    db.query(ListModel).filter(
        and_(
            ListModel.board_id == lst.board_id,
            ListModel.id != lst.id,
            ListModel.position >= lst.position
        )
    ).update({"position": ListModel.position + 1})
    db.commit()


def _reposition_after_update(db: Session, lst: ListModel, old_position: int) -> None:
    """Reposition lists after updating a list's position.

    Args:
        db: Database session
        lst: The updated list
        old_position: The old position of the list
    """
    if lst.position > old_position:
        # Moving down: shift lists between old and new position up
        db.query(ListModel).filter(
            and_(
                ListModel.board_id == lst.board_id,
                ListModel.id != lst.id,
                ListModel.position > old_position,
                ListModel.position <= lst.position
            )
        ).update({"position": ListModel.position - 1})
    else:
        # Moving up: shift lists between new and old position down
        db.query(ListModel).filter(
            and_(
                ListModel.board_id == lst.board_id,
                ListModel.id != lst.id,
                ListModel.position >= lst.position,
                ListModel.position < old_position
            )
        ).update({"position": ListModel.position + 1})

    db.commit()

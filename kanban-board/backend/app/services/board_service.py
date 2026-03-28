"""Board service layer for business logic."""
import uuid
from typing import Literal
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from fastapi import HTTPException, status

from app.models.board import Board
from app.models.board_member import BoardMember
from app.models.list import List
from app.models.card import Card
from app.models.user import User
from app.schemas.board import BoardCreate, BoardUpdate, BoardMemberRole


def check_board_access(
    db: Session,
    board_id: uuid.UUID | str,
    user_id: uuid.UUID | str,
    require_role: Literal["owner", "admin", "member", "viewer"] | None = None,
) -> BoardMember | None:
    """Check if user has access to a board.

    Args:
        db: Database session
        board_id: Board ID
        user_id: User ID
        require_role: Minimum required role (owner > admin > member > viewer)

    Returns:
        BoardMember if user has access, None otherwise

    Raises:
        HTTPException: If user doesn't have required access
    """
    # Convert UUID to string if needed
    board_id_str = str(board_id) if isinstance(board_id, uuid.UUID) else board_id
    user_id_str = str(user_id) if isinstance(user_id, uuid.UUID) else user_id

    member = db.query(BoardMember).filter(
        and_(
            BoardMember.board_id == board_id_str,
            BoardMember.user_id == user_id_str
        )
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found or access denied",
        )

    if require_role:
        role_hierarchy = {"owner": 4, "admin": 3, "member": 2, "viewer": 1}
        if role_hierarchy.get(member.role, 0) < role_hierarchy.get(require_role, 0):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Requires {require_role} role or higher.",
            )

    return member


def get_board_by_id(db: Session, board_id: uuid.UUID | str, user_id: uuid.UUID | str) -> Board:
    """Get a board by ID with access check.

    Args:
        db: Database session
        board_id: Board ID
        user_id: User ID

    Returns:
        Board object

    Raises:
        HTTPException: If board not found or access denied
    """
    # Convert UUID to string if needed
    board_id_str = str(board_id) if isinstance(board_id, uuid.UUID) else board_id

    member = check_board_access(db, board_id_str, user_id)
    return db.query(Board).filter(Board.id == board_id_str).first()


def get_boards_for_user(
    db: Session,
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 20,
    include_archived: bool = False,
) -> tuple[list[Board], int]:
    """Get all boards for a user.

    Args:
        db: Database session
        user_id: User ID
        skip: Number of records to skip
        limit: Maximum number of records to return
        include_archived: Whether to include archived boards

    Returns:
        Tuple of (boards list, total count)
    """
    # Get board IDs where user is a member
    board_ids_query = select(BoardMember.board_id).where(
        BoardMember.user_id == user_id
    )
    board_ids = [row[0] for row in db.execute(board_ids_query).all()]

    if not board_ids:
        return [], 0

    # Build query
    query = db.query(Board).filter(Board.id.in_(board_ids))

    if not include_archived:
        query = query.filter(Board.is_archived == False)

    # Get total count
    total = query.count()

    # Get paginated results
    boards = query.order_by(Board.updated_at.desc()).offset(skip).limit(limit).all()

    return boards, total


def create_board(db: Session, board_data: BoardCreate, owner_id: uuid.UUID) -> Board:
    """Create a new board.

    Args:
        db: Database session
        board_data: Board creation data
        owner_id: User ID of the board owner

    Returns:
        Created Board object
    """
    # Create board
    board = Board(
        title=board_data.title,
        description=board_data.description,
        background_color=board_data.background_color,
        background_url=board_data.background_url,
        is_public=board_data.is_public,
        owner_id=owner_id,
    )
    db.add(board)
    db.flush()  # Flush to get the board ID

    # Add owner as a board member with owner role
    member = BoardMember(
        board_id=board.id,
        user_id=owner_id,
        role="owner"
    )
    db.add(member)

    db.commit()
    db.refresh(board)
    return board


def update_board(
    db: Session,
    board_id: uuid.UUID,
    board_data: BoardUpdate,
    user_id: uuid.UUID,
) -> Board:
    """Update a board.

    Args:
        db: Database session
        board_id: Board ID
        board_data: Board update data
        user_id: User ID of the user making the update

    Returns:
        Updated Board object

    Raises:
        HTTPException: If board not found or access denied
    """
    # Check access - need at least member role to update
    member = check_board_access(db, board_id, user_id, require_role="member")

    board = db.query(Board).filter(Board.id == board_id).first()

    # Update fields
    update_data = board_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(board, field, value)

    db.commit()
    db.refresh(board)
    return board


def delete_board(db: Session, board_id: uuid.UUID, user_id: uuid.UUID) -> None:
    """Delete a board.

    Args:
        db: Database session
        board_id: Board ID
        user_id: User ID of the user making the deletion

    Raises:
        HTTPException: If board not found or access denied
    """
    # Check access - only owner can delete
    check_board_access(db, board_id, user_id, require_role="owner")

    board = db.query(Board).filter(Board.id == board_id).first()
    db.delete(board)
    db.commit()


def add_board_member(
    db: Session,
    board_id: uuid.UUID,
    member_data: BoardMemberRole,
    inviter_id: uuid.UUID,
) -> BoardMember:
    """Add a member to a board.

    Args:
        db: Database session
        board_id: Board ID
        member_data: Member data (user_id and role)
        inviter_id: User ID of the user inviting the member

    Returns:
        Created BoardMember object

    Raises:
        HTTPException: If access denied, user not found, or already a member
    """
    # Check access - need admin role to add members
    check_board_access(db, board_id, inviter_id, require_role="admin")

    # Verify target user exists
    target_user = db.query(User).filter(User.id == member_data.user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Check if user is already a member
    existing_member = db.query(BoardMember).filter(
        and_(
            BoardMember.board_id == board_id,
            BoardMember.user_id == member_data.user_id
        )
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this board",
        )

    # Cannot add another owner
    if member_data.role == "owner":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add another owner. There can be only one owner per board.",
        )

    # Create member
    member = BoardMember(
        board_id=board_id,
        user_id=member_data.user_id,
        role=member_data.role
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def remove_board_member(
    db: Session,
    board_id: uuid.UUID,
    target_user_id: uuid.UUID,
    requester_id: uuid.UUID,
) -> None:
    """Remove a member from a board.

    Args:
        db: Database session
        board_id: Board ID
        target_user_id: User ID of the member to remove
        requester_id: User ID of the user making the request

    Raises:
        HTTPException: If access denied or user not found
    """
    # Allow users to remove themselves
    if target_user_id == requester_id:
        check_board_access(db, board_id, requester_id)
    else:
        # Need admin role to remove others
        check_board_access(db, board_id, requester_id, require_role="admin")

    # Check if target is owner
    target_member = db.query(BoardMember).filter(
        and_(
            BoardMember.board_id == board_id,
            BoardMember.user_id == target_user_id
        )
    ).first()

    if not target_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )

    if target_member.role == "owner":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove the board owner",
        )

    db.delete(target_member)
    db.commit()


def update_board_member_role(
    db: Session,
    board_id: uuid.UUID,
    target_user_id: uuid.UUID,
    new_role: str,
    requester_id: uuid.UUID,
) -> BoardMember:
    """Update a board member's role.

    Args:
        db: Database session
        board_id: Board ID
        target_user_id: User ID of the member
        new_role: New role to assign
        requester_id: User ID of the user making the request

    Returns:
        Updated BoardMember object

    Raises:
        HTTPException: If access denied or invalid role
    """
    # Only owner can change roles
    check_board_access(db, board_id, requester_id, require_role="owner")

    if new_role not in ["owner", "admin", "member", "viewer"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be one of: owner, admin, member, viewer",
        )

    member = db.query(BoardMember).filter(
        and_(
            BoardMember.board_id == board_id,
            BoardMember.user_id == target_user_id
        )
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )

    # Cannot change owner role
    if member.role == "owner":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change the owner's role",
        )

    # Cannot promote to owner
    if new_role == "owner":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot promote to owner. Transfer ownership instead.",
        )

    member.role = new_role
    db.commit()
    db.refresh(member)
    return member


def get_board_stats(db: Session, board_id: uuid.UUID) -> dict:
    """Get statistics for a board.

    Args:
        db: Database session
        board_id: Board ID

    Returns:
        Dictionary with board statistics
    """
    members_count = db.query(BoardMember).filter(
        BoardMember.board_id == board_id
    ).count()

    lists_count = db.query(List).filter(
        and_(List.board_id == board_id, List.is_archived == False)
    ).count()

    # Get cards count through lists
    list_ids = [l.id for l in db.query(List.id).filter(List.board_id == board_id).all()]
    cards_count = 0
    if list_ids:
        cards_count = db.query(Card).filter(Card.list_id.in_(list_ids)).count()

    return {
        "members_count": members_count,
        "lists_count": lists_count,
        "cards_count": cards_count,
    }

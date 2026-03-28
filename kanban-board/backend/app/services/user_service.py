"""User service layer for business logic."""
import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.security import verify_password, get_password_hash
from app.core.config import settings


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """Get a user by username."""
    return db.query(User).filter(User.username == username).first()


def create_user(
    db: Session,
    email: str,
    username: str,
    password: str,
    full_name: str | None = None,
) -> User:
    """Create a new user with hashed password."""
    # Check if user with email already exists
    if get_user_by_email(db, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Check if user with username already exists
    if get_user_by_username(db, username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # Create new user with hashed password
    user = User(
        email=email,
        username=username,
        password_hash=get_password_hash(password),
        full_name=full_name,
        is_active=True,
        is_verified=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """Authenticate a user by username and password.

    Returns the user if authentication is successful, None otherwise.
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    return user


def update_user(
    db: Session,
    user: User,
    email: str | None = None,
    full_name: str | None = None,
    avatar_url: str | None = None,
) -> User:
    """Update user information."""
    if email is not None and email != user.email:
        # Check if email is already taken by another user
        existing_user = get_user_by_email(db, email)
        if existing_user and existing_user.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        user.email = email

    if full_name is not None:
        user.full_name = full_name

    if avatar_url is not None:
        user.avatar_url = avatar_url

    db.commit()
    db.refresh(user)
    return user


def create_refresh_token_db(db: Session, user: User, token: str) -> RefreshToken:
    """Create a refresh token in the database."""
    # Calculate expiration date
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    # Create refresh token
    refresh_token = RefreshToken(
        token=token,
        user_id=user.id,
        expires_at=expires_at,
    )
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return refresh_token


def validate_refresh_token(db: Session, token: str) -> RefreshToken | None:
    """Validate a refresh token from the database.

    Returns the token if valid, None otherwise.
    """
    refresh_token = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()

    if not refresh_token:
        return None

    if not refresh_token.is_valid():
        return None

    return refresh_token


def revoke_refresh_token(db: Session, token: str) -> bool:
    """Revoke a refresh token.

    Returns True if the token was revoked, False if not found.
    """
    refresh_token = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()

    if not refresh_token:
        return False

    refresh_token.revoke()
    db.commit()
    return True


def revoke_user_tokens(db: Session, user: User) -> None:
    """Revoke all refresh tokens for a user."""
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id,
        RefreshToken.revoked_at.is_(None)
    ).update({"revoked_at": datetime.now(timezone.utc)})
    db.commit()


def cleanup_expired_tokens(db: Session) -> int:
    """Remove expired refresh tokens from the database.

    Returns the number of tokens removed.
    """
    now = datetime.now(timezone.utc)
    deleted_count = db.query(RefreshToken).filter(
        RefreshToken.expires_at < now
    ).delete()
    db.commit()
    return deleted_count

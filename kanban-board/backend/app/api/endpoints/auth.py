"""Authentication API endpoints."""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import DBSession, CurrentUser
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    TokenResponse,
    RefreshTokenRequest,
    AuthResponse,
)
from app.services import user_service

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: DBSession,
) -> AuthResponse:
    """Register a new user and return tokens.

    - **email**: User's email address (must be unique)
    - **username**: Desired username (must be unique, 3-50 characters)
    - **password**: Password (min 8 characters)
    - **full_name**: User's full name (optional)
    """
    user = user_service.create_user(
        db=db,
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
        full_name=user_data.full_name,
    )
    
    access_token = create_access_token(subject=str(user.id))
    refresh_token_jti = create_refresh_token(subject=str(user.id))
    user_service.create_refresh_token_db(db, user, refresh_token_jti)

    return AuthResponse(
        user=UserResponse.model_validate(user),
        access_token=access_token,
        refresh_token=refresh_token_jti,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    user_data: UserLogin,
    db: DBSession,
) -> TokenResponse:
    """Authenticate user and return tokens.

    - **username**: Username or email
    - **password**: User's password

    Returns both access_token and refresh_token.
    """
    # Try to authenticate with username or email
    user = user_service.get_user_by_username(db, user_data.username)
    if not user:
        user = user_service.get_user_by_email(db, user_data.username)

    if not user or not user_service.authenticate_user(db, user.username, user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(subject=str(user.id))

    # Create refresh token
    refresh_token_jti = create_refresh_token(subject=str(user.id))
    user_service.create_refresh_token_db(db, user, refresh_token_jti)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_jti,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    token_data: RefreshTokenRequest,
    db: DBSession,
) -> TokenResponse:
    """Refresh access token using refresh token.

    - **refresh_token**: Valid refresh token from login

    Returns new access_token and refresh_token.
    """
    # Validate refresh token from database
    refresh_token_db = user_service.validate_refresh_token(db, token_data.refresh_token)
    if not refresh_token_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user = user_service.get_user_by_id(db, refresh_token_db.user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    # Revoke old refresh token
    user_service.revoke_refresh_token(db, token_data.refresh_token)

    # Create new tokens
    access_token = create_access_token(subject=str(user.id))
    new_refresh_token = create_refresh_token(subject=str(user.id))
    user_service.create_refresh_token_db(db, user, new_refresh_token)

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/logout")
async def logout(
    token_data: RefreshTokenRequest,
    db: DBSession,
) -> dict[str, str]:
    """Logout user and revoke refresh token.

    - **refresh_token**: Refresh token to revoke
    """
    success = user_service.revoke_refresh_token(db, token_data.refresh_token)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found",
        )

    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: CurrentUser,
) -> User:
    """Get current authenticated user information."""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: CurrentUser,
    db: DBSession,
) -> User:
    """Update current user information.

    - **email**: New email address (optional)
    - **full_name**: New full name (optional)
    - **avatar_url**: New avatar URL (optional)
    """
    updated_user = user_service.update_user(
        db=db,
        user=current_user,
        email=user_data.email,
        full_name=user_data.full_name,
        avatar_url=user_data.avatar_url,
    )
    return updated_user

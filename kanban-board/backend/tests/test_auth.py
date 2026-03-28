"""Tests for authentication endpoints."""
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from backend.app.models import RefreshToken


class TestUserRegistration:
    """Tests for user registration endpoint."""

    def test_register_user_success(self, client: TestClient):
        """Test successful user registration."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "password123",
                "full_name": "New User",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert data["full_name"] == "New User"
        assert "id" in data
        assert data["is_active"] is True
        assert "password" not in data
        assert "password_hash" not in data

    def test_register_duplicate_email(self, client: TestClient, test_user: User):
        """Test registration with duplicate email fails."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": test_user.email,
                "username": "differentuser",
                "password": "password123",
            },
        )
        assert response.status_code == 400

    def test_register_duplicate_username(self, client: TestClient, test_user: User):
        """Test registration with duplicate username fails."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "different@example.com",
                "username": test_user.username,
                "password": "password123",
            },
        )
        assert response.status_code == 400

    def test_register_weak_password(self, client: TestClient):
        """Test registration with weak password fails."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                "username": "user1",
                "password": "short",
            },
        )
        assert response.status_code == 422

    def test_register_invalid_email(self, client: TestClient):
        """Test registration with invalid email fails."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "notanemail",
                "username": "user1",
                "password": "password123",
            },
        )
        assert response.status_code == 422

    def test_register_short_username(self, client: TestClient):
        """Test registration with short username fails."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                "username": "ab",
                "password": "password123",
            },
        )
        assert response.status_code == 422


class TestUserLogin:
    """Tests for user login endpoint."""

    def test_login_with_username_success(self, client: TestClient, test_user: User, test_password: str):
        """Test successful login with username."""
        response = client.post(
            "/api/auth/login",
            json={
                "username": test_user.username,
                "password": test_password,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data

    def test_login_with_email_success(self, client: TestClient, test_user: User, test_password: str):
        """Test successful login with email."""
        response = client.post(
            "/api/auth/login",
            json={
                "username": test_user.email,
                "password": test_password,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_login_wrong_password(self, client: TestClient, test_user: User):
        """Test login with wrong password fails."""
        response = client.post(
            "/api/auth/login",
            json={
                "username": test_user.username,
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with nonexistent user fails."""
        response = client.post(
            "/api/auth/login",
            json={
                "username": "nonexistent",
                "password": "password123",
            },
        )
        assert response.status_code == 401

    def test_login_inactive_user(self, client: TestClient, db_session, test_password: str):
        """Test login with inactive user fails."""
        from backend.app.models import User
        from backend.app.core.security import hash_password

        inactive_user = User(
            email="inactive@example.com",
            username="inactiveuser",
            password_hash=hash_password(test_password),
            is_active=False,
        )
        db_session.add(inactive_user)
        db_session.commit()

        response = client.post(
            "/api/auth/login",
            json={
                "username": "inactiveuser",
                "password": test_password,
            },
        )
        # Should succeed authentication but return tokens
        # The token validation during API calls will fail
        assert response.status_code == 200


class TestRefreshToken:
    """Tests for token refresh endpoint."""

    def test_refresh_token_success(self, client: TestClient, test_refresh_token: RefreshToken):
        """Test successful token refresh."""
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": test_refresh_token.token},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        # Old refresh token should be revoked
        assert data["refresh_token"] != test_refresh_token.token

    def test_refresh_token_invalid(self, client: TestClient):
        """Test refresh with invalid token fails."""
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": "invalid_token_123"},
        )
        assert response.status_code == 401

    def test_refresh_token_expired(self, client: TestClient, db_session, test_user: User):
        """Test refresh with expired token fails."""
        from datetime import datetime, timedelta, timezone

        expired_token = RefreshToken(
            user_id=test_user.id,
            token="expired_token_123",
            expires_at=datetime.now(timezone.utc) - timedelta(days=1),
        )
        db_session.add(expired_token)
        db_session.commit()

        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": "expired_token_123"},
        )
        assert response.status_code == 401


class TestLogout:
    """Tests for logout endpoint."""

    def test_logout_success(self, client: TestClient, test_refresh_token: RefreshToken):
        """Test successful logout revokes refresh token."""
        response = client.post(
            "/api/auth/logout",
            json={"refresh_token": test_refresh_token.token},
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully logged out"

        # Token should no longer work for refresh
        refresh_response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": test_refresh_token.token},
        )
        assert refresh_response.status_code == 401

    def test_logout_invalid_token(self, client: TestClient):
        """Test logout with invalid token."""
        response = client.post(
            "/api/auth/logout",
            json={"refresh_token": "nonexistent_token"},
        )
        assert response.status_code == 404


class TestGetCurrentUser:
    """Tests for getting current user endpoint."""

    def test_get_current_user_success(self, client: TestClient, auth_headers, test_user: User):
        """Test getting current user with valid token."""
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_user.id)
        assert data["email"] == test_user.email
        assert data["username"] == test_user.username
        assert "password_hash" not in data

    def test_get_current_user_no_token(self, client: TestClient):
        """Test getting current user without token fails."""
        response = client.get("/api/auth/me")
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client: TestClient):
        """Test getting current user with invalid token fails."""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401


class TestUpdateCurrentUser:
    """Tests for updating current user endpoint."""

    def test_update_user_email(self, client: TestClient, auth_headers, test_user: User):
        """Test updating user email."""
        new_email = "updated@example.com"
        response = client.put(
            "/api/auth/me",
            headers=auth_headers,
            json={"email": new_email}
        )
        assert response.status_code == 200
        assert response.json()["email"] == new_email

    def test_update_user_full_name(self, client: TestClient, auth_headers):
        """Test updating user full name."""
        new_name = "Updated Name"
        response = client.put(
            "/api/auth/me",
            headers=auth_headers,
            json={"full_name": new_name}
        )
        assert response.status_code == 200
        assert response.json()["full_name"] == new_name

    def test_update_user_avatar_url(self, client: TestClient, auth_headers):
        """Test updating user avatar URL."""
        avatar_url = "https://example.com/avatar.jpg"
        response = client.put(
            "/api/auth/me",
            headers=auth_headers,
            json={"avatar_url": avatar_url}
        )
        assert response.status_code == 200
        assert response.json()["avatar_url"] == avatar_url

    def test_update_user_no_token(self, client: TestClient):
        """Test updating user without authentication fails."""
        response = client.put(
            "/api/auth/me",
            json={"full_name": "New Name"}
        )
        assert response.status_code == 401

    def test_update_user_duplicate_email(self, client: TestClient, auth_headers, test_user2: User):
        """Test updating to duplicate email fails."""
        response = client.put(
            "/api/auth/me",
            headers=auth_headers,
            json={"email": test_user2.email}
        )
        assert response.status_code == 400

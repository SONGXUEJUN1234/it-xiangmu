"""Tests for comment and label endpoints."""
import uuid
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from backend.app.models import Comment, Label


class TestCommentEndpoints:
    """Tests for comment CRUD operations."""

    def test_create_comment(self, client: TestClient, auth_headers, test_card: Card):
        """Test creating a new comment."""
        response = client.post(
            f"/api/comments",
            headers=auth_headers,
            json={
                "card_id": str(test_card.id),
                "content": "This is a test comment",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "This is a test comment"
        assert data["card_id"] == str(test_card.id)
        assert "id" in data

    def test_get_comments_by_card(self, client: TestClient, auth_headers, test_card: Card, test_comment: Comment):
        """Test getting comments for a card."""
        response = client.get(
            f"/api/comments?card_id={test_card.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "data" in data
        assert len(data["data"]) >= 1

    def test_get_comment_by_id(self, client: TestClient, auth_headers, test_comment: Comment):
        """Test getting a specific comment."""
        response = client.get(f"/api/comments/{test_comment.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_comment.id)
        assert data["content"] == test_comment.content

    def test_update_comment(self, client: TestClient, auth_headers, test_comment: Comment):
        """Test updating a comment."""
        response = client.put(
            f"/api/comments/{test_comment.id}",
            headers=auth_headers,
            json={"content": "Updated comment content"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Updated comment content"
        assert data["is_edited"] is True

    def test_delete_comment(self, client: TestClient, auth_headers, db_session, test_card: Card, test_user: User):
        """Test deleting a comment."""
        # Create a comment to delete
        comment = Comment(
            card_id=test_card.id,
            user_id=test_user.id,
            content="Comment to delete",
        )
        db_session.add(comment)
        db_session.commit()

        response = client.delete(f"/api/comments/{comment.id}", headers=auth_headers)
        assert response.status_code == 204

    def test_create_reply(self, client: TestClient, auth_headers, test_comment: Comment, test_card: Card):
        """Test creating a reply to a comment."""
        response = client.post(
            f"/api/comments",
            headers=auth_headers,
            json={
                "card_id": str(test_card.id),
                "content": "This is a reply",
                "parent_id": str(test_comment.id),
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "This is a reply"
        assert data["parent_id"] == str(test_comment.id)

    def test_delete_comment_unauthorized(self, client: TestClient, auth_headers2, test_comment: Comment):
        """Test that a user cannot delete another user's comment."""
        response = client.delete(f"/api/comments/{test_comment.id}", headers=auth_headers2)
        # Should either fail or the endpoint should check ownership
        # Assuming the endpoint checks ownership
        assert response.status_code in [403, 404]


class TestLabelEndpoints:
    """Tests for label CRUD operations."""

    def test_create_label(self, client: TestClient, auth_headers, test_board: Board):
        """Test creating a new label."""
        response = client.post(
            f"/api/labels",
            headers=auth_headers,
            json={
                "board_id": str(test_board.id),
                "name": "Feature",
                "color": "#3b82f6",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Feature"
        assert data["color"] == "#3b82f6"
        assert data["board_id"] == str(test_board.id)

    def test_get_labels_by_board(self, client: TestClient, auth_headers, test_board: Board, test_label: Label):
        """Test getting labels for a board."""
        response = client.get(
            f"/api/labels?board_id={test_board.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "data" in data
        assert len(data["data"]) >= 1

    def test_get_label_by_id(self, client: TestClient, auth_headers, test_label: Label):
        """Test getting a specific label."""
        response = client.get(f"/api/labels/{test_label.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_label.id)
        assert data["name"] == test_label.name

    def test_update_label(self, client: TestClient, auth_headers, test_label: Label):
        """Test updating a label."""
        response = client.put(
            f"/api/labels/{test_label.id}",
            headers=auth_headers,
            json={
                "name": "Updated Label Name",
                "color": "#ff0000",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Label Name"
        assert data["color"] == "#ff0000"

    def test_delete_label(self, client: TestClient, auth_headers, db_session, test_board: Board):
        """Test deleting a label."""
        # Create a label to delete
        label = Label(
            board_id=test_board.id,
            name="Label to Delete",
            color="#000000",
        )
        db_session.add(label)
        db_session.commit()

        response = client.delete(f"/api/labels/{label.id}", headers=auth_headers)
        assert response.status_code == 204

    def test_add_label_to_card(self, client: TestClient, auth_headers, test_card: Card, test_label: Label):
        """Test adding a label to a card."""
        response = client.post(
            f"/api/cards/{test_card.id}/labels/{test_label.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        # Should return the updated card with labels
        assert "id" in data

    def test_remove_label_from_card(self, client: TestClient, auth_headers, db_session, test_card: Card, test_label: Label):
        """Test removing a label from a card."""
        # First add the label to the card
        from backend.app.models import CardLabel
        card_label = CardLabel(
            card_id=test_card.id,
            label_id=test_label.id,
        )
        db_session.add(card_label)
        db_session.commit()

        # Then remove it
        response = client.delete(
            f"/api/cards/{test_card.id}/labels/{test_label.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200

    def test_create_label_invalid_color(self, client: TestClient, auth_headers, test_board: Board):
        """Test creating a label with invalid color format."""
        response = client.post(
            f"/api/labels",
            headers=auth_headers,
            json={
                "board_id": str(test_board.id),
                "name": "Invalid Label",
                "color": "not-a-color",
            },
        )
        assert response.status_code == 422


class TestActivityEndpoints:
    """Tests for activity log endpoints."""

    def test_get_board_activities(self, client: TestClient, auth_headers, test_board: Board):
        """Test getting activity log for a board."""
        response = client.get(
            f"/api/activities?board_id={test_board.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "data" in data

    def test_get_activities_pagination(self, client: TestClient, auth_headers, test_board: Board):
        """Test activity log pagination."""
        response = client.get(
            f"/api/activities?board_id={test_board.id}&page=1&limit=10",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "pagination" in data


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_health_check(self, client: TestClient):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_root_endpoint(self, client: TestClient):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data

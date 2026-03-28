"""Tests for board, list, and card endpoints."""
import uuid

import pytest
from fastapi.testclient import TestClient

from backend.app.models import Board, List, Card


class TestBoardEndpoints:
    """Tests for board CRUD operations."""

    def test_create_board(self, client: TestClient, auth_headers):
        """Test creating a new board."""
        response = client.post(
            "/api/boards",
            headers=auth_headers,
            json={
                "title": "New Board",
                "description": "A new test board",
                "is_public": False,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Board"
        assert data["description"] == "A new test board"
        assert data["is_public"] is False
        assert "id" in data

    def test_get_boards(self, client: TestClient, auth_headers, test_board: Board):
        """Test getting all boards for user."""
        response = client.get("/api/boards", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "data" in data
        assert "pagination" in data
        assert len(data["data"]) >= 1

    def test_get_board_by_id(self, client: TestClient, auth_headers, test_board: Board):
        """Test getting a specific board."""
        response = client.get(f"/api/boards/{test_board.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_board.id)
        assert data["title"] == test_board.title

    def test_get_board_unauthorized(self, client: TestClient, test_board: Board):
        """Test getting a board without authentication fails."""
        response = client.get(f"/api/boards/{test_board.id}")
        assert response.status_code == 401

    def test_update_board(self, client: TestClient, auth_headers, test_board: Board):
        """Test updating a board."""
        response = client.put(
            f"/api/boards/{test_board.id}",
            headers=auth_headers,
            json={
                "title": "Updated Board Title",
                "description": "Updated description",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Board Title"
        assert data["description"] == "Updated description"

    def test_delete_board(self, client: TestClient, auth_headers, db_session, test_user: User):
        """Test deleting a board."""
        # Create a board to delete
        board = Board(
            title="Board to Delete",
            owner_id=test_user.id,
        )
        db_session.add(board)
        db_session.commit()

        response = client.delete(f"/api/boards/{board.id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify board is deleted
        get_response = client.get(f"/api/boards/{board.id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_get_board_members(self, client: TestClient, auth_headers, test_board: Board):
        """Test getting board members."""
        response = client.get(f"/api/boards/{test_board.id}/members", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_add_board_member(self, client: TestClient, auth_headers, test_board: Board, test_user2: User):
        """Test adding a member to a board."""
        response = client.post(
            f"/api/boards/{test_board.id}/members",
            headers=auth_headers,
            json={
                "user_id": str(test_user2.id),
                "role": "member",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == str(test_user2.id)

    def test_remove_board_member(self, client: TestClient, auth_headers, test_board: Board, test_user2: User, db_session):
        """Test removing a member from a board."""
        from backend.app.models import BoardMember

        # First add the member
        member = BoardMember(
            board_id=test_board.id,
            user_id=test_user2.id,
            role="member",
        )
        db_session.add(member)
        db_session.commit()

        # Then remove them
        response = client.delete(
            f"/api/boards/{test_board.id}/members/{test_user2.id}",
            headers=auth_headers,
        )
        assert response.status_code == 204

    def test_update_board_member_role(self, client: TestClient, auth_headers, test_board: Board, test_user2: User, db_session):
        """Test updating a board member's role."""
        from backend.app.models import BoardMember

        # First add the member
        member = BoardMember(
            board_id=test_board.id,
            user_id=test_user2.id,
            role="member",
        )
        db_session.add(member)
        db_session.commit()

        # Update their role
        response = client.patch(
            f"/api/boards/{test_board.id}/members/{test_user2.id}",
            headers=auth_headers,
            json={"role": "admin"},
        )
        assert response.status_code == 200


class TestListEndpoints:
    """Tests for list CRUD operations."""

    def test_create_list(self, client: TestClient, auth_headers, test_board: Board):
        """Test creating a new list."""
        response = client.post(
            "/api/lists",
            headers=auth_headers,
            json={
                "board_id": str(test_board.id),
                "title": "In Progress",
                "position": 1,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "In Progress"
        assert data["position"] == 1
        assert data["board_id"] == str(test_board.id)

    def test_get_lists_by_board(self, client: TestClient, auth_headers, test_board: Board, test_list: List):
        """Test getting lists for a board."""
        response = client.get(
            f"/api/lists?board_id={test_board.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "data" in data
        assert len(data["data"]) >= 1

    def test_update_list(self, client: TestClient, auth_headers, test_list: List):
        """Test updating a list."""
        response = client.put(
            f"/api/lists/{test_list.id}",
            headers=auth_headers,
            json={"title": "Updated List Title"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated List Title"

    def test_delete_list(self, client: TestClient, auth_headers, db_session, test_board: Board):
        """Test deleting a list."""
        # Create a list to delete
        list_obj = List(
            board_id=test_board.id,
            title="List to Delete",
            position=99,
        )
        db_session.add(list_obj)
        db_session.commit()

        response = client.delete(f"/api/lists/{list_obj.id}", headers=auth_headers)
        assert response.status_code == 204


class TestCardEndpoints:
    """Tests for card CRUD operations."""

    def test_create_card(self, client: TestClient, auth_headers, test_list: List, test_user: User):
        """Test creating a new card."""
        response = client.post(
            "/api/cards",
            headers=auth_headers,
            json={
                "list_id": str(test_list.id),
                "title": "New Card",
                "description": "A new test card",
                "position": 1,
                "priority": "high",
                "assignee_id": str(test_user.id),
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Card"
        assert data["description"] == "A new test card"
        assert data["priority"] == "high"

    def test_get_cards_by_list(self, client: TestClient, auth_headers, test_list: List, test_card: Card):
        """Test getting cards for a list."""
        response = client.get(
            f"/api/cards?list_id={test_list.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "data" in data
        assert len(data["data"]) >= 1

    def test_get_card_by_id(self, client: TestClient, auth_headers, test_card: Card):
        """Test getting a specific card."""
        response = client.get(f"/api/cards/{test_card.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_card.id)
        assert data["title"] == test_card.title

    def test_update_card(self, client: TestClient, auth_headers, test_card: Card):
        """Test updating a card."""
        response = client.put(
            f"/api/cards/{test_card.id}",
            headers=auth_headers,
            json={
                "title": "Updated Card Title",
                "priority": "critical",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Card Title"
        assert data["priority"] == "critical"

    def test_move_card(self, client: TestClient, auth_headers, test_card: Card):
        """Test moving a card to a different position/list."""
        response = client.post(
            f"/api/cards/{test_card.id}/move",
            headers=auth_headers,
            json={
                "list_id": str(test_card.list_id),
                "position": 5,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["position"] == 5

    def test_assign_card(self, client: TestClient, auth_headers, test_card: Card, test_user2: User):
        """Test assigning a card to a user."""
        response = client.post(
            f"/api/cards/{test_card.id}/assign",
            headers=auth_headers,
            json={"assignee_id": str(test_user2.id)},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["assignee_id"] == str(test_user2.id)

    def test_unassign_card(self, client: TestClient, auth_headers, test_card: Card):
        """Test unassigning a card."""
        response = client.post(
            f"/api/cards/{test_card.id}/assign",
            headers=auth_headers,
            json={"assignee_id": None},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["assignee_id"] is None

    def test_complete_card(self, client: TestClient, auth_headers, test_card: Card):
        """Test marking a card as completed."""
        response = client.post(
            f"/api/cards/{test_card.id}/complete",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_completed"] is True
        assert data["completed_at"] is not None

    def test_uncomplete_card(self, client: TestClient, auth_headers, test_card: Card, db_session):
        """Test marking a card as incomplete."""
        # First mark as completed
        test_card.is_completed = True
        test_card.completed_at = datetime.now(timezone.utc)
        db_session.commit()

        response = client.delete(
            f"/api/cards/{test_card.id}/complete",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_completed"] is False

    def test_delete_card(self, client: TestClient, auth_headers, db_session, test_list: List):
        """Test deleting a card."""
        # Create a card to delete
        from datetime import datetime, timezone
        from backend.app.core.security import hash_password

        # Get test user for assignment
        from backend.app.models import User
        test_user = db_session.query(User).first()

        card = Card(
            list_id=test_list.id,
            title="Card to Delete",
            position=99,
            assignee_id=test_user.id if test_user else None,
        )
        db_session.add(card)
        db_session.commit()

        response = client.delete(f"/api/cards/{card.id}", headers=auth_headers)
        assert response.status_code == 204


class TestCardSearch:
    """Tests for card search functionality."""

    def test_search_cards_by_query(self, client: TestClient, auth_headers, test_card: Card):
        """Test searching cards by title/description."""
        response = client.post(
            "/api/cards/search",
            headers=auth_headers,
            json={"query": "Test"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "data" in data
        assert len(data["data"]) >= 1

    def test_search_cards_by_priority(self, client: TestClient, auth_headers, test_card: Card):
        """Test searching cards by priority."""
        response = client.post(
            "/api/cards/search",
            headers=auth_headers,
            json={"priority": "high"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "success" in data

    def test_search_cards_by_assignee(self, client: TestClient, auth_headers, test_card: Card, test_user: User):
        """Test searching cards by assignee."""
        response = client.post(
            "/api/cards/search",
            headers=auth_headers,
            json={"assignee_id": str(test_user.id)},
        )
        assert response.status_code == 200
        data = response.json()
        assert "success" in data

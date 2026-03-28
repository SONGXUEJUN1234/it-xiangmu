"""Pytest configuration and fixtures for the Kanban Board API tests."""
import os
import tempfile
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.app.core.database import Base, get_db
from backend.app.models import User, Board, List, Card, Label, Comment, RefreshToken
from backend.app.core.security import hash_password
from backend.app.main import app


# Use an in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
    """Create a test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    return engine


@pytest.fixture(scope="function")
def db_session(engine) -> Generator[Session, None, None]:
    """Create a new database session for each test."""
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session: Session):
    """Create a test client with database session override."""
    def _get_test_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_password() -> str:
    """Return a test password."""
    return "testpassword123"


@pytest.fixture
def test_user(db_session: Session, test_password: str) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=hash_password(test_password),
        full_name="Test User",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user2(db_session: Session, test_password: str) -> User:
    """Create a second test user."""
    user = User(
        email="test2@example.com",
        username="testuser2",
        password_hash=hash_password(test_password),
        full_name="Test User 2",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(client: TestClient, test_user: User, test_password: str):
    """Get authentication headers for a test user."""
    response = client.post(
        "/api/auth/login",
        json={"username": test_user.username, "password": test_password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers2(client: TestClient, test_user2: User, test_password: str):
    """Get authentication headers for a second test user."""
    response = client.post(
        "/api/auth/login",
        json={"username": test_user2.username, "password": test_password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_board(db_session: Session, test_user: User) -> Board:
    """Create a test board."""
    board = Board(
        title="Test Board",
        description="A test board for testing",
        owner_id=test_user.id,
        is_public=False,
    )
    db_session.add(board)
    db_session.commit()
    db_session.refresh(board)
    return board


@pytest.fixture
def test_list(db_session: Session, test_board: Board) -> List:
    """Create a test list."""
    list_obj = List(
        board_id=test_board.id,
        title="To Do",
        position=0,
    )
    db_session.add(list_obj)
    db_session.commit()
    db_session.refresh(list_obj)
    return list_obj


@pytest.fixture
def test_card(db_session: Session, test_list: List, test_user: User) -> Card:
    """Create a test card."""
    card = Card(
        list_id=test_list.id,
        title="Test Card",
        description="A test card for testing",
        position=0,
        priority="high",
        assignee_id=test_user.id,
    )
    db_session.add(card)
    db_session.commit()
    db_session.refresh(card)
    return card


@pytest.fixture
def test_label(db_session: Session, test_board: Board) -> Label:
    """Create a test label."""
    label = Label(
        board_id=test_board.id,
        name="Bug",
        color="#ef4444",
    )
    db_session.add(label)
    db_session.commit()
    db_session.refresh(label)
    return label


@pytest.fixture
def test_comment(db_session: Session, test_card: Card, test_user: User) -> Comment:
    """Create a test comment."""
    comment = Comment(
        card_id=test_card.id,
        user_id=test_user.id,
        content="This is a test comment",
    )
    db_session.add(comment)
    db_session.commit()
    db_session.refresh(comment)
    return comment


@pytest.fixture
def test_refresh_token(db_session: Session, test_user: User) -> RefreshToken:
    """Create a test refresh token."""
    from datetime import datetime, timedelta, timezone

    token = RefreshToken(
        user_id=test_user.id,
        token="test_refresh_token_123",
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )
    db_session.add(token)
    db_session.commit()
    db_session.refresh(token)
    return token

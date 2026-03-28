#!/usr/bin/env python3
"""Database initialization script for the Kanban Board application.

This script creates all database tables and optionally seeds them with sample data.
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.database import Base, SessionLocal
from backend.app.core.security import hash_password
from backend.app.models import (
    User,
    Board,
    List,
    Card,
    Label,
    BoardMember,
    Comment,
    Activity,
)


def create_tables() -> None:
    """Create all database tables."""
    print("Creating database tables...")
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def drop_tables() -> None:
    """Drop all database tables."""
    print("Dropping database tables...")
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped successfully!")


def seed_database() -> None:
    """Seed the database with sample data for development."""
    print("Seeding database with sample data...")

    db: Session = SessionLocal()

    try:
        # Create test users
        print("Creating test users...")
        user1 = User(
            email="user1@example.com",
            username="user1",
            password_hash=hash_password("password123"),
            full_name="Test User 1",
            is_active=True,
            is_verified=True,
        )
        user2 = User(
            email="user2@example.com",
            username="user2",
            password_hash=hash_password("password123"),
            full_name="Test User 2",
            is_active=True,
            is_verified=True,
        )
        db.add(user1)
        db.add(user2)
        db.flush()

        # Create a board
        print("Creating test board...")
        board1 = Board(
            title="Project Alpha",
            description="Main project board for development team",
            owner_id=user1.id,
            is_public=False,
            is_archived=False,
        )
        db.add(board1)
        db.flush()

        # Add user2 as a board member
        board_member = BoardMember(
            board_id=board1.id,
            user_id=user2.id,
            role="member",
        )
        db.add(board_member)

        # Create lists
        print("Creating test lists...")
        todo_list = List(
            board_id=board1.id,
            title="To Do",
            position=0,
        )
        in_progress_list = List(
            board_id=board1.id,
            title="In Progress",
            position=1,
        )
        done_list = List(
            board_id=board1.id,
            title="Done",
            position=2,
        )
        db.add(todo_list)
        db.add(in_progress_list)
        db.add(done_list)
        db.flush()

        # Create labels
        print("Creating test labels...")
        label1 = Label(
            board_id=board1.id,
            name="Bug",
            color="#ef4444",  # Red
        )
        label2 = Label(
            board_id=board1.id,
            name="Feature",
            color="#3b82f6",  # Blue
        )
        label3 = Label(
            board_id=board1.id,
            name="Urgent",
            color="#f59e0b",  # Orange
        )
        db.add(label1)
        db.add(label2)
        db.add(label3)
        db.flush()

        # Create cards
        print("Creating test cards...")
        card1 = Card(
            list_id=todo_list.id,
            title="Set up project structure",
            description="Initialize the project with proper folder structure and configuration files.",
            position=0,
            priority="high",
            assignee_id=user1.id,
        )
        card2 = Card(
            list_id=in_progress_list.id,
            title="Implement user authentication",
            description="Add JWT-based authentication with register and login endpoints.",
            position=0,
            priority="high",
            assignee_id=user2.id,
        )
        card3 = Card(
            list_id=done_list.id,
            title="Create database models",
            description="Define SQLAlchemy models for User, Board, List, and Card entities.",
            position=0,
            priority="medium",
            assignee_id=user1.id,
            is_completed=True,
        )
        db.add(card1)
        db.add(card2)
        db.add(card3)
        db.flush()

        # Create comments
        print("Creating test comments...")
        comment1 = Comment(
            card_id=card1.id,
            user_id=user2.id,
            content="Don't forget to add environment configuration!",
        )
        comment2 = Comment(
            card_id=card2.id,
            user_id=user1.id,
            content="I'll help with the JWT token refresh logic.",
        )
        db.add(comment1)
        db.add(comment2)

        db.commit()
        print("Database seeded successfully!")
        print("\nTest accounts created:")
        print("  - user1@example.com / password123")
        print("  - user2@example.com / password123")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


def main() -> None:
    """Main entry point for the script."""
    import argparse

    parser = argparse.ArgumentParser(description="Initialize the Kanban Board database")
    parser.add_argument(
        "--drop", action="store_true", help="Drop existing tables before creating"
    )
    parser.add_argument("--seed", action="store_true", help="Seed database with sample data")
    parser.add_argument("--seed-only", action="store_true", help="Only seed data, don't create tables")

    args = parser.parse_args()

    if args.seed_only:
        seed_database()
    else:
        if args.drop:
            drop_tables()
        create_tables()
        if args.seed:
            seed_database()


if __name__ == "__main__":
    main()

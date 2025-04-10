import os
import pytest
from unittest.mock import patch, MagicMock
from app.database.database import get_engine, Base, SessionLocal


def test_get_engine_sqlite(monkeypatch):
    """
    Test that the SQLite engine is created successfully.
    This test temporarily sets the DATABASE_URL environment variable to an SQLite in-memory database
    and verifies that the engine is created correctly.
    """
    # Temporarily set the DATABASE_URL to SQLite in-memory
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    # Verify that the environment variable is updated
    assert os.getenv("DATABASE_URL") == "sqlite:///:memory:"
    # Patch the DATABASE_URL and test engine creation
    with patch("app.database.database.DATABASE_URL", "sqlite:///:memory:"):
        engine = get_engine()
        assert engine is not None
        assert "sqlite" in str(engine.url)


def test_get_engine_postgresql(monkeypatch):
    """
    Test that the PostgreSQL engine is created successfully.
    This test temporarily sets the DATABASE_URL environment variable to a PostgreSQL database
    and verifies that the engine is created correctly.
    """
    # Temporarily set the DATABASE_URL to PostgreSQL
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/test_db"
    )
    # Verify that the environment variable is updated
    assert (
        os.getenv("DATABASE_URL")
        == "postgresql+psycopg2://user:password@localhost:5432/test_db"
    )
    # Patch the DATABASE_URL and test engine creation
    with patch(
        "app.database.database.DATABASE_URL",
        "postgresql+psycopg2://user:password@localhost:5432/test_db",
    ):
        engine = get_engine()
        assert engine is not None
        assert "postgresql" in str(engine.url)


def test_get_engine_invalid_url(monkeypatch):
    """
    Test that an invalid DATABASE_URL raises an ArgumentError.
    This test sets an invalid DATABASE_URL and verifies that an exception is raised
    when attempting to create the engine.
    """
    # Temporarily set the DATABASE_URL to an invalid value
    monkeypatch.setenv("DATABASE_URL", "invalid_url")
    # Verify that the environment variable is updated
    assert os.getenv("DATABASE_URL") == "invalid_url"
    # Patch the DATABASE_URL and test for exception
    with patch("app.database.database.DATABASE_URL", "invalid_url"):
        with pytest.raises(
            Exception, match="Could not parse SQLAlchemy URL from string 'invalid_url'"
        ):
            get_engine()


def test_session_local():
    """
    Test that a session can be created and closed successfully.
    This test verifies that the SessionLocal object can create a session
    and that the session can be closed without errors.
    """
    session = SessionLocal()
    assert session is not None
    session.close()


def test_base_metadata():
    """
    Test that the Base metadata is initialized correctly.
    This test ensures that the Base metadata object is not None,
    indicating that the database models are properly defined.
    """
    assert Base.metadata is not None


def test_engine_initialization_success():
    """
    Test that the database engine is initialized successfully.
    This test mocks the get_engine function to ensure that the engine
    is initialized without errors.
    """
    with patch("app.database.database.get_engine") as mock_get_engine:
        mock_get_engine.return_value = MagicMock()
        engine = get_engine()
        assert engine is not None

import os
import pytest
from unittest.mock import patch, MagicMock
from app.database.database import get_engine, Base, SessionLocal


def test_get_engine_sqlite(monkeypatch):
    """
    Test that the SQLite engine is created successfully.
    """
    monkeypatch.setenv(
        "DATABASE_URL", "sqlite:///:memory:"
    )  # Тимчасово встановлюємо SQLite
    assert (
        os.getenv("DATABASE_URL") == "sqlite:///:memory:"
    )  # Перевіряємо, чи змінна оновлена
    with patch("app.database.database.DATABASE_URL", "sqlite:///:memory:"):
        engine = get_engine()
        assert engine is not None
        assert "sqlite" in str(engine.url)


def test_get_engine_postgresql(monkeypatch):
    """
    Test that the PostgreSQL engine is created successfully.
    """
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/test_db"
    )
    assert (
        os.getenv("DATABASE_URL")
        == "postgresql+psycopg2://user:password@localhost:5432/test_db"
    )
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
    """
    monkeypatch.setenv("DATABASE_URL", "invalid_url")
    assert os.getenv("DATABASE_URL") == "invalid_url"  # Перевіряємо, чи змінна оновлена
    with patch("app.database.database.DATABASE_URL", "invalid_url"):
        with pytest.raises(
            Exception, match="Could not parse SQLAlchemy URL from string 'invalid_url'"
        ):
            get_engine()


def test_session_local():
    """
    Test that a session can be created and closed successfully.
    """
    session = SessionLocal()
    assert session is not None
    session.close()


def test_base_metadata():
    """
    Test that the Base metadata is initialized correctly.
    """
    assert Base.metadata is not None


def test_engine_initialization_success():
    """
    Test that the database engine is initialized successfully.
    """
    with patch("app.database.database.get_engine") as mock_get_engine:
        mock_get_engine.return_value = MagicMock()
        engine = get_engine()
        assert engine is not None

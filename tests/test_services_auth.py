import pytest
from unittest.mock import MagicMock
from app.services.auth import authenticate_user, hash_password, create_access_token
from app.models.user import User


def test_authenticate_user_success():
    """
    Test successful user authentication.
    """
    mock_user = User(
        id=1,
        email="test@example.com",
        hashed_password=hash_password("Password123"),
        is_active=True,
        is_verified=True,
    )

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    result = authenticate_user(mock_db, "test@example.com", "Password123")
    assert result == mock_user


def test_authenticate_user_invalid_password():
    """
    Test authentication failure due to invalid password.
    """
    mock_user = User(
        id=1,
        email="test@example.com",
        hashed_password=hash_password("Password123"),
        is_active=True,
        is_verified=True,
    )

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    result = authenticate_user(mock_db, "test@example.com", "WrongPassword")
    assert result is None


def test_authenticate_user_not_found():
    """
    Test authentication failure due to user not found.
    """
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = authenticate_user(mock_db, "nonexistent@example.com", "Password123")
    assert result is None


def test_create_access_token():
    """
    Test creation of access token.
    """
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    assert token is not None

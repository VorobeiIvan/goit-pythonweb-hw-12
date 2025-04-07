import pytest
from unittest.mock import MagicMock
from app.services.auth import authenticate_user, hash_password
from app.models.user import User


def test_authenticate_user_success():
    """
    Test successful user authentication.
    """
    # Моканий користувач
    mock_user = User(
        id=1,
        email="test@example.com",
        hashed_password=hash_password("Password123"),
        is_active=True,
        is_verified=True,
    )

    # Мокаємо базу даних
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    # Викликаємо функцію
    result = authenticate_user(mock_db, "test@example.com", "Password123")

    # Перевіряємо результат
    assert result == mock_user


def test_authenticate_user_invalid_password():
    """
    Test authentication failure due to invalid password.
    """
    # Моканий користувач
    mock_user = User(
        id=1,
        email="test@example.com",
        hashed_password=hash_password("Password123"),
        is_active=True,
        is_verified=True,
    )

    # Мокаємо базу даних
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    # Викликаємо функцію з неправильним паролем
    result = authenticate_user(mock_db, "test@example.com", "WrongPassword")

    # Перевіряємо результат
    assert result is None


def test_authenticate_user_not_found():
    """
    Test authentication failure due to user not found.
    """
    # Мокаємо базу даних
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Викликаємо функцію
    result = authenticate_user(mock_db, "nonexistent@example.com", "Password123")

    # Перевіряємо результат
    assert result is None

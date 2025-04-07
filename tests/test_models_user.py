import pytest
from datetime import datetime, timezone
from app.models.user import User, UserRole


def test_user_model():
    """
    Test the SQLAlchemy User model.
    """
    user = User(
        id=1,
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
        is_verified=False,
        role=UserRole.USER,
        created_at=datetime(2023, 1, 1, tzinfo=timezone.utc),
        updated_at=datetime(2023, 1, 2, tzinfo=timezone.utc),
    )

    assert user.id == 1
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_password"
    assert user.is_active is True
    assert user.is_verified is False
    assert user.role == UserRole.USER
    assert user.created_at == datetime(2023, 1, 1, tzinfo=timezone.utc)
    assert user.updated_at == datetime(2023, 1, 2, tzinfo=timezone.utc)


def test_user_role_enum():
    """
    Test the UserRole enum.
    """
    assert UserRole.USER == "user"
    assert UserRole.ADMIN == "admin"

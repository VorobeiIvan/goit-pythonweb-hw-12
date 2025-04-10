import pytest
from datetime import datetime, timezone
from app.models.user import User, UserRole


def test_user_model():
    """
    Test the SQLAlchemy User model to ensure it correctly initializes and stores attributes.
    """
    # Create a User instance with test data
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

    # Assert that all attributes are correctly set
    assert user.id == 1  # Check user ID
    assert user.email == "test@example.com"  # Check email
    assert user.hashed_password == "hashed_password"  # Check hashed password
    assert user.is_active is True  # Check if the user is active
    assert user.is_verified is False  # Check if the user is not verified
    assert user.role == UserRole.USER  # Check user role
    assert user.created_at == datetime(2023, 1, 1, tzinfo=timezone.utc)  # Check creation timestamp
    assert user.updated_at == datetime(2023, 1, 2, tzinfo=timezone.utc)  # Check update timestamp


def test_user_role_enum():
    """
    Test the UserRole enum to ensure it contains the correct values.
    """
    # Assert that the UserRole enum values are as expected
    assert UserRole.USER == "user"  # Check the 'USER' role value
    assert UserRole.ADMIN == "admin"  # Check the 'ADMIN' role value

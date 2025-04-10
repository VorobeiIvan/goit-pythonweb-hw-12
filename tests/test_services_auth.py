import pytest
from unittest.mock import MagicMock
from app.services.auth import authenticate_user, hash_password, create_access_token
from app.models.user import User


def test_authenticate_user_success():
    """
    Test case: Successful user authentication.
    Description: This test verifies that the `authenticate_user` function correctly authenticates a user 
    when provided with valid credentials (email and password).
    """
    # Mock user object with valid credentials
    mock_user = User(
        id=1,
        email="test@example.com",
        hashed_password=hash_password("Password123"),
        is_active=True,
        is_verified=True,
    )

    # Mock database query to return the mock user
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    # Call the function and assert the result
    result = authenticate_user(mock_db, "test@example.com", "Password123")
    assert result == mock_user


def test_authenticate_user_invalid_password():
    """
    Test case: Authentication failure due to invalid password.
    Description: This test ensures that the `authenticate_user` function returns None 
    when the provided password does not match the stored hashed password.
    """
    # Mock user object with valid credentials
    mock_user = User(
        id=1,
        email="test@example.com",
        hashed_password=hash_password("Password123"),
        is_active=True,
        is_verified=True,
    )

    # Mock database query to return the mock user
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    # Call the function with an invalid password and assert the result
    result = authenticate_user(mock_db, "test@example.com", "WrongPassword")
    assert result is None


def test_authenticate_user_not_found():
    """
    Test case: Authentication failure due to user not found.
    Description: This test verifies that the `authenticate_user` function returns None 
    when no user is found in the database for the provided email.
    """
    # Mock database query to return None (user not found)
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Call the function with a non-existent user and assert the result
    result = authenticate_user(mock_db, "nonexistent@example.com", "Password123")
    assert result is None


def test_create_access_token():
    """
    Test case: Creation of access token.
    Description: This test ensures that the `create_access_token` function generates a valid token 
    when provided with the required data payload.
    """
    # Data payload for the token
    data = {"sub": "test@example.com"}

    # Call the function to create an access token
    token = create_access_token(data)

    # Assert that the token is not None (successfully created)
    assert token is not None

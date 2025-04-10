from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.services.auth import create_access_token
import pytest


def test_get_current_user_not_found():
    """
    Test case to verify that `get_current_user` raises an HTTPException
    with status code 401 when the user is not found in the database or cache.
    """
    # Mock the database session
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Mock the Redis client
    mock_redis_client = MagicMock()
    mock_redis_client.get.return_value = None

    # Patch Redis client and JWT decode function
    with patch("app.utils.dependencies.redis_client", mock_redis_client), patch(
        "app.utils.dependencies.jwt.decode", return_value={"sub": "test@example.com"}
    ):
        # Expect an HTTPException to be raised
        with pytest.raises(HTTPException) as exc_info:
            get_current_user("mock_token", db=mock_db)
        # Assert the exception details
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid token"


def test_get_current_user_from_cache():
    """
    Test case to verify that `get_current_user` retrieves the user
    from the Redis cache when available.
    """
    # Mock the database session
    mock_db = MagicMock()
    # Mock the Redis client
    mock_redis_client = MagicMock()

    # Create a valid JWT token
    valid_token = create_access_token({"sub": "test@example.com"})

    # Mock Redis to return a cached user
    mock_redis_client.get.return_value = '{"id": 1, "email": "test@example.com"}'

    # Patch Redis client
    with patch("app.utils.dependencies.redis_client", mock_redis_client):
        # Call the function and retrieve the user
        user = get_current_user(valid_token, db=mock_db)
        # Assert the user's email matches the cached data
        assert user.email == "test@example.com"

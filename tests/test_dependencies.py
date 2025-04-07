from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.services.auth import create_access_token
import pytest


def test_get_current_user_not_found():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    mock_redis_client = MagicMock()
    mock_redis_client.get.return_value = None

    with patch("app.utils.dependencies.redis_client", mock_redis_client), patch(
        "app.utils.dependencies.jwt.decode", return_value={"sub": "test@example.com"}
    ):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user("mock_token", db=mock_db)
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid token"


def test_get_current_user_from_cache():
    mock_db = MagicMock()
    mock_redis_client = MagicMock()

    # Створення дійсного JWT токена
    valid_token = create_access_token({"sub": "test@example.com"})

    # Мок Redis, щоб повернути кешованого користувача
    mock_redis_client.get.return_value = '{"id": 1, "email": "test@example.com"}'

    with patch("app.utils.dependencies.redis_client", mock_redis_client):
        user = get_current_user(valid_token, db=mock_db)
        assert user.email == "test@example.com"

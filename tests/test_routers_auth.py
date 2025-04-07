from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.auth import get_password_hash
from main import app
import pytest

client = TestClient(app)


@pytest.fixture
def setup_test_user():
    """
    Створення тестового користувача в базі даних.
    """
    db = MagicMock()
    test_user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password"),
        is_active=True,
        is_verified=True,
    )
    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.return_value = test_user
    yield test_user


def test_login_success(setup_test_user):
    with patch("app.services.auth.authenticate_user", return_value=setup_test_user):
        response = client.post(
            "/auth/token",
            data={"username": "test@example.com", "password": "password"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()


def test_login_failure():
    with patch("app.services.auth.authenticate_user", return_value=None):
        response = client.post(
            "/auth/token",
            data={"username": "wrong@example.com", "password": "wrong_password"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"


def test_password_reset_request(setup_test_user):
    with patch("app.services.email.send_password_reset_email") as mock_send_email:
        response = client.post(
            "/auth/password-reset-request", json={"email": "test@example.com"}
        )
        assert response.status_code == 200
        assert (
            response.json()["message"]
            == "Password reset link has been sent to your email."
        )
        mock_send_email.assert_called_once()

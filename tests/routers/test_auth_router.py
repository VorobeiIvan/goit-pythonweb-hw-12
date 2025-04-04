import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def test_user_data():
    """
    Фікстура для створення тестових даних користувача.
    """
    return {
        "email": "test@example.com",
        "password": "securepassword",
    }


def test_register_user(test_user_data):
    """
    Тест для перевірки реєстрації нового користувача.
    """
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 201, "User registration failed"
    data = response.json()
    assert "id" in data, "Response does not contain user ID"
    assert data["email"] == test_user_data["email"], "Email does not match"


def test_login_user(test_user_data):
    """
    Тест для перевірки логіну користувача.
    """
    # Спочатку реєструємо користувача
    client.post("/auth/register", json=test_user_data)

    # Потім виконуємо логін
    response = client.post("/auth/login", data=test_user_data)
    assert response.status_code == 200, "User login failed"
    data = response.json()
    assert "access_token" in data, "Response does not contain access token"
    assert data["token_type"] == "bearer", "Token type does not match"


def test_login_invalid_user():
    """
    Тест для перевірки логіну з невалідними даними.
    """
    invalid_data = {
        "email": "invalid@example.com",
        "password": "wrongpassword",
    }
    response = client.post("/auth/login", data=invalid_data)
    assert response.status_code == 401, "Invalid login should return 401"
    assert (
        response.json()["detail"] == "Invalid credentials"
    ), "Error message does not match"

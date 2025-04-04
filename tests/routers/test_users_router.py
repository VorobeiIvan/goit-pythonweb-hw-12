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
        "email": "testuser@example.com",
        "password": "securepassword",
        "first_name": "John",
        "last_name": "Doe",
    }


def test_get_current_user(test_user_data):
    """
    Тест для перевірки отримання поточного користувача.
    """
    # Спочатку реєструємо користувача
    register_response = client.post("/auth/register", json=test_user_data)
    assert register_response.status_code == 201, "User registration failed"

    # Логін користувача
    login_response = client.post("/auth/login", data=test_user_data)
    assert login_response.status_code == 200, "User login failed"
    access_token = login_response.json()["access_token"]

    # Отримання поточного користувача
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200, "Failed to fetch current user"
    data = response.json()
    assert data["email"] == test_user_data["email"], "Email does not match"
    assert (
        data["first_name"] == test_user_data["first_name"]
    ), "First name does not match"
    assert data["last_name"] == test_user_data["last_name"], "Last name does not match"


def test_get_current_user_unauthorized():
    """
    Тест для перевірки отримання поточного користувача без авторизації.
    """
    response = client.get("/users/me")
    assert response.status_code == 401, "Unauthorized request should return 401"
    assert (
        response.json()["detail"] == "Not authenticated"
    ), "Error message does not match"

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


@pytest.fixture
def auth_headers(test_user_data):
    """
    Фікстура для отримання заголовків авторизації.
    """
    # Реєстрація користувача
    client.post("/auth/register", json=test_user_data)

    # Логін користувача
    login_response = client.post("/auth/login", data=test_user_data)
    access_token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


def test_get_current_user(auth_headers, test_user_data):
    """
    Тест для перевірки отримання поточного користувача.
    """
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200, "Failed to fetch current user"
    data = response.json()
    assert data["email"] == test_user_data["email"], "Email does not match"
    assert (
        data["first_name"] == test_user_data["first_name"]
    ), "First name does not match"
    assert data["last_name"] == test_user_data["last_name"], "Last name does not match"


def test_update_user(auth_headers, test_user_data):
    """
    Тест для перевірки оновлення даних користувача.
    """
    updated_data = {
        "first_name": "UpdatedJohn",
        "last_name": "UpdatedDoe",
    }
    response = client.put("/users/me", json=updated_data, headers=auth_headers)
    assert response.status_code == 200, "Failed to update user"
    data = response.json()
    assert (
        data["first_name"] == updated_data["first_name"]
    ), "First name was not updated"
    assert data["last_name"] == updated_data["last_name"], "Last name was not updated"


def test_delete_user(auth_headers):
    """
    Тест для перевірки видалення користувача.
    """
    response = client.delete("/users/me", headers=auth_headers)
    assert response.status_code == 204, "Failed to delete user"

    # Перевіряємо, що користувач більше не існує
    get_response = client.get("/users/me", headers=auth_headers)
    assert get_response.status_code == 401, "Deleted user should not be accessible"

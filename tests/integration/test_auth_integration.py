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
        "email": "integration_test@example.com",
        "password": "securepassword",
    }


def test_auth_integration_flow(test_user_data):
    """
    Інтеграційний тест для перевірки повного циклу аутентифікації.
    """
    # 1. Реєстрація нового користувача
    register_response = client.post("/auth/register", json=test_user_data)
    assert register_response.status_code == 201, "User registration failed"
    register_data = register_response.json()
    assert "id" in register_data, "Response does not contain user ID"
    assert register_data["email"] == test_user_data["email"], "Email does not match"

    # 2. Логін користувача
    login_response = client.post("/auth/login", data=test_user_data)
    assert login_response.status_code == 200, "User login failed"
    login_data = login_response.json()
    assert "access_token" in login_data, "Response does not contain access token"
    assert login_data["token_type"] == "bearer", "Token type does not match"

    # 3. Отримання поточного користувача
    access_token = login_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    me_response = client.get("/users/me", headers=headers)
    assert me_response.status_code == 200, "Failed to fetch current user"
    me_data = me_response.json()
    assert me_data["email"] == test_user_data["email"], "Email does not match"

    # 4. Логін із неправильним паролем
    invalid_login_response = client.post(
        "/auth/login",
        data={"email": test_user_data["email"], "password": "wrongpassword"},
    )
    assert invalid_login_response.status_code == 401, "Invalid login should return 401"
    assert (
        invalid_login_response.json()["detail"] == "Invalid credentials"
    ), "Error message does not match"

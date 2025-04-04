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
    }


@pytest.fixture
def test_contact_data():
    """
    Фікстура для створення тестових даних контакту.
    """
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
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


def test_create_contact(auth_headers, test_contact_data):
    """
    Тест для перевірки створення нового контакту.
    """
    response = client.post("/contacts/", json=test_contact_data, headers=auth_headers)
    assert response.status_code == 201, "Contact creation failed"
    data = response.json()
    assert "id" in data, "Response does not contain contact ID"
    assert (
        data["first_name"] == test_contact_data["first_name"]
    ), "First name does not match"
    assert (
        data["last_name"] == test_contact_data["last_name"]
    ), "Last name does not match"
    assert data["email"] == test_contact_data["email"], "Email does not match"
    assert data["phone"] == test_contact_data["phone"], "Phone does not match"


def test_get_contact(auth_headers, test_contact_data):
    """
    Тест для перевірки отримання контакту за ID.
    """
    # Створюємо контакт
    create_response = client.post(
        "/contacts/", json=test_contact_data, headers=auth_headers
    )
    contact_id = create_response.json()["id"]

    # Отримуємо контакт за ID
    response = client.get(f"/contacts/{contact_id}", headers=auth_headers)
    assert response.status_code == 200, "Failed to fetch contact by ID"
    data = response.json()
    assert data["id"] == contact_id, "Contact ID does not match"
    assert data["email"] == test_contact_data["email"], "Email does not match"


def test_delete_contact(auth_headers, test_contact_data):
    """
    Тест для перевірки видалення контакту.
    """
    # Створюємо контакт
    create_response = client.post(
        "/contacts/", json=test_contact_data, headers=auth_headers
    )
    contact_id = create_response.json()["id"]

    # Видаляємо контакт
    delete_response = client.delete(f"/contacts/{contact_id}", headers=auth_headers)
    assert delete_response.status_code == 204, "Failed to delete contact"

    # Перевіряємо, що контакт видалено
    get_response = client.get(f"/contacts/{contact_id}", headers=auth_headers)
    assert get_response.status_code == 404, "Contact was not deleted"

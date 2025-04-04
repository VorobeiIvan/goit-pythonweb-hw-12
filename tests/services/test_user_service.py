import pytest
from app.services.user import create_user, get_user_by_email
from app.models.user import User
from app.schemas.user import UserCreate


@pytest.fixture
def test_user_data():
    """
    Фікстура для створення тестових даних користувача.
    """
    return {
        "email": "test@example.com",
        "password": "securepassword",
        "first_name": "Test",
        "last_name": "User",
    }


def test_create_user(db_session, test_user_data):
    """
    Тест для перевірки створення нового користувача.
    """
    user_data = UserCreate(**test_user_data)
    user = create_user(db_session, user_data)

    assert user is not None, "User creation failed"
    assert user.email == test_user_data["email"], "Email does not match"
    assert user.first_name == test_user_data["first_name"], "First name does not match"
    assert user.last_name == test_user_data["last_name"], "Last name does not match"


def test_get_user_by_email(db_session, test_user_data):
    """
    Тест для перевірки отримання користувача за email.
    """
    # Спочатку створюємо користувача
    user_data = UserCreate(**test_user_data)
    created_user = create_user(db_session, user_data)

    # Потім отримуємо користувача за email
    fetched_user = get_user_by_email(db_session, test_user_data["email"])

    assert fetched_user is not None, "User not found"
    assert fetched_user.id == created_user.id, "User ID does not match"
    assert fetched_user.email == created_user.email, "Email does not match"

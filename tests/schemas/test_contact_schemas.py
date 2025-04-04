import pytest
from app.services.contact import (
    create_contact,
    get_contact_by_id,
    delete_contact,
)
from app.schemas.contact import ContactCreate
from app.models.contact import Contact


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


def test_create_contact(db_session, test_contact_data):
    """
    Тест для перевірки створення нового контакту.
    """
    contact_data = ContactCreate(**test_contact_data)
    contact = create_contact(db_session, contact_data)

    assert contact is not None, "Contact creation failed"
    assert (
        contact.first_name == test_contact_data["first_name"]
    ), "First name does not match"
    assert (
        contact.last_name == test_contact_data["last_name"]
    ), "Last name does not match"
    assert contact.email == test_contact_data["email"], "Email does not match"
    assert contact.phone == test_contact_data["phone"], "Phone does not match"


def test_get_contact_by_id(db_session, test_contact_data):
    """
    Тест для перевірки отримання контакту за ID.
    """
    # Спочатку створюємо контакт
    contact_data = ContactCreate(**test_contact_data)
    created_contact = create_contact(db_session, contact_data)

    # Потім отримуємо контакт за ID
    fetched_contact = get_contact_by_id(db_session, created_contact.id)

    assert fetched_contact is not None, "Contact not found"
    assert fetched_contact.id == created_contact.id, "Contact ID does not match"
    assert fetched_contact.email == created_contact.email, "Email does not match"


def test_delete_contact(db_session, test_contact_data):
    """
    Тест для перевірки видалення контакту.
    """
    # Спочатку створюємо контакт
    contact_data = ContactCreate(**test_contact_data)
    created_contact = create_contact(db_session, contact_data)

    # Видаляємо контакт
    delete_contact(db_session, created_contact.id)

    # Перевіряємо, що контакт видалено
    deleted_contact = get_contact_by_id(db_session, created_contact.id)
    assert deleted_contact is None, "Contact was not deleted"

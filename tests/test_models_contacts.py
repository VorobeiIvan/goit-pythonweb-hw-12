import pytest
from datetime import date, datetime, timedelta, timezone
from app.models.contacts import ContactCreate, Contact


def test_contact_create_valid_birthday():
    """
    Test that a valid birthday is accepted.
    """
    valid_birthday = date.today() - timedelta(days=365 * 25)  # 25 років тому
    contact = ContactCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        birthday=valid_birthday,
    )
    assert contact.birthday == valid_birthday


def test_contact_create_invalid_birthday():
    """
    Test that a birthday in the future raises a ValueError.
    """
    future_birthday = date.today() + timedelta(days=1)  # Завтрашня дата
    with pytest.raises(ValueError, match="Birthday cannot be in the future."):
        ContactCreate(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            phone="0987654321",
            birthday=future_birthday,
        )

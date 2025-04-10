import pytest
from datetime import date, timedelta
from app.models.contacts import ContactCreate, Contact


def test_contact_create_valid_birthday():
    """
    Test that a valid birthday is accepted.
    This test ensures that the `ContactCreate` model correctly accepts a valid birthday
    that is in the past (e.g., 25 years ago).
    """
    valid_birthday = date.today() - timedelta(days=365 * 25)  # 25 years ago
    contact = ContactCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        birthday=valid_birthday,
    )
    # Assert that the birthday is correctly set
    assert contact.birthday == valid_birthday


def test_contact_create_invalid_birthday():
    """
    Test that a birthday in the future raises a ValueError.
    This test ensures that the `ContactCreate` model raises an appropriate error
    when a birthday is set to a future date.
    """
    future_birthday = date.today() + timedelta(days=1)  # Tomorrow's date
    with pytest.raises(ValueError, match="Birthday cannot be in the future."):
        ContactCreate(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            phone="0987654321",
            birthday=future_birthday,
        )

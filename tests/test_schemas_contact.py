import pytest
from datetime import date, timedelta
from app.schemas.contact import ContactCreate, ContactResponse


def test_contact_create_valid_data():
    """
    Test that a valid ContactCreate instance is created successfully.
    This test ensures that all fields are correctly assigned when valid data is provided.
    """
    valid_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "birthday": date.today() - timedelta(days=365 * 25),  # 25 years ago
        "additional_info": "Friend from college",
    }
    contact = ContactCreate(**valid_data)
    # Assert that all fields match the input data
    assert contact.first_name == valid_data["first_name"]
    assert contact.last_name == valid_data["last_name"]
    assert contact.email == valid_data["email"]
    assert contact.phone == valid_data["phone"]
    assert contact.birthday == valid_data["birthday"]
    assert contact.additional_info == valid_data["additional_info"]


def test_contact_create_invalid_birthday():
    """
    Test that a future birthday raises a ValueError.
    This test ensures that the validation logic prevents setting a birthday in the future.
    """
    invalid_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone": "0987654321",
        "birthday": date.today() + timedelta(days=1),  # Tomorrow's date
    }
    # Expect a ValueError with a specific error message
    with pytest.raises(ValueError, match="Birthday cannot be in the future."):
        ContactCreate(**invalid_data)


def test_contact_create_invalid_phone():
    """
    Test that an invalid phone number raises a ValueError.
    This test ensures that the phone number validation logic works as expected.
    """
    invalid_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com",
        "phone": "abc123",  # Invalid format
        "birthday": date.today() - timedelta(days=365 * 30),  # 30 years ago
    }
    # Expect a ValueError with a specific error message
    with pytest.raises(
        ValueError,
        match="Phone number must contain only digits and be 7-15 characters long.",
    ):
        ContactCreate(**invalid_data)


def test_contact_response():
    """
    Test that a valid ContactResponse instance is created successfully.
    This test ensures that all fields are correctly assigned when valid data is provided.
    """
    valid_data = {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "birthday": date.today() - timedelta(days=365 * 25),  # 25 years ago
        "additional_info": "Friend from college",
    }
    contact_response = ContactResponse(**valid_data)
    # Assert that all fields match the input data
    assert contact_response.id == valid_data["id"]
    assert contact_response.first_name == valid_data["first_name"]
    assert contact_response.last_name == valid_data["last_name"]
    assert contact_response.email == valid_data["email"]
    assert contact_response.phone == valid_data["phone"]
    assert contact_response.birthday == valid_data["birthday"]
    assert contact_response.additional_info == valid_data["additional_info"]

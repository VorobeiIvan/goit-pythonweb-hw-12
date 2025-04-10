import pytest
from app.schemas.user import UserCreate, UserResponse, Token, UserRole


def test_user_create_valid_data():
    """
    Test that a valid UserCreate instance is created successfully.
    
    This test verifies that when valid data is provided, a UserCreate object
    is instantiated correctly with all attributes matching the input data.
    """
    valid_data = {
        "email": "test@example.com",
        "password": "Password123",
        "is_active": True,
        "is_verified": False,
        "role": UserRole.USER,
    }
    user = UserCreate(**valid_data)
    assert user.email == valid_data["email"]
    assert user.password == valid_data["password"]
    assert user.is_active == valid_data["is_active"]
    assert user.is_verified == valid_data["is_verified"]
    assert user.role == valid_data["role"]


def test_user_create_invalid_password_too_short():
    """
    Test that a ValueError is raised for a password shorter than 8 characters.
    
    This test ensures that the password validation logic correctly identifies
    and rejects passwords that do not meet the minimum length requirement.
    """
    invalid_data = {
        "email": "test@example.com",
        "password": "Short1",
    }
    with pytest.raises(
        ValueError, match="Password must be at least 8 characters long."
    ):
        UserCreate(**invalid_data)


def test_user_create_invalid_password_no_digit():
    """
    Test that a ValueError is raised for a password without any digits.
    
    This test ensures that the password validation logic correctly identifies
    and rejects passwords that do not contain at least one numeric character.
    """
    invalid_data = {
        "email": "test@example.com",
        "password": "Password",
    }
    with pytest.raises(ValueError, match="Password must contain at least one digit."):
        UserCreate(**invalid_data)


def test_user_create_invalid_password_no_letter():
    """
    Test that a ValueError is raised for a password without any letters.
    
    This test ensures that the password validation logic correctly identifies
    and rejects passwords that do not contain at least one alphabetic character.
    """
    invalid_data = {
        "email": "test@example.com",
        "password": "12345678",
    }
    with pytest.raises(ValueError, match="Password must contain at least one letter."):
        UserCreate(**invalid_data)


def test_user_response():
    """
    Test that a valid UserResponse instance is created successfully.
    
    This test verifies that when valid data is provided, a UserResponse object
    is instantiated correctly with all attributes matching the input data.
    """
    valid_data = {
        "id": 1,
        "email": "test@example.com",
        "is_verified": True,
    }
    user_response = UserResponse(**valid_data)
    assert user_response.id == valid_data["id"]
    assert user_response.email == valid_data["email"]
    assert user_response.is_verified == valid_data["is_verified"]


def test_token():
    """
    Test that a valid Token instance is created successfully.
    
    This test verifies that when valid data is provided, a Token object
    is instantiated correctly with all attributes matching the input data.
    """
    valid_data = {
        "access_token": "someaccesstoken",
        "token_type": "bearer",
    }
    token = Token(**valid_data)
    assert token.access_token == valid_data["access_token"]
    assert token.token_type == valid_data["token_type"]

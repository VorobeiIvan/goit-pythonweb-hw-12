from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from enum import Enum
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Base class for SQLAlchemy models
Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model representing a user in the database.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier for the user
    email = Column(
        String, unique=True, index=True, nullable=False
    )  # User's email address
    hashed_password = Column(
        String, nullable=False
    )  # Hashed password for authentication
    is_active = Column(Boolean, default=True)  # Indicates if the user is active
    is_verified = Column(
        Boolean, default=False
    )  # Indicates if the user's email is verified
    role = Column(String, default="user")  # Role of the user (e.g., user, admin)
    created_at = Column(
        DateTime, default=datetime.now(timezone.utc)
    )  # Timestamp of user creation


class UserRole(str, Enum):
    """
    Enumeration of available user roles.
    """

    USER = "user"  # Regular user role
    ADMIN = "admin"  # Administrator role


class UserBase(BaseModel):
    """
    Base schema for user-related data.
    Defines common fields for user operations.
    """

    email: EmailStr  # User's email address
    is_active: Optional[bool] = True  # Indicates if the user is active
    is_verified: Optional[bool] = False  # Indicates if the user's email is verified
    role: Optional[UserRole] = UserRole.USER  # Role of the user

    class ConfigDict:
        from_attributes = True  # Allows mapping from ORM models
        arbitrary_types_allowed = True  # Allows custom types


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    Extends UserBase and adds a password field.
    """

    password: str  # Plaintext password for the new user

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        """
        Validates the password to ensure it meets security requirements.

        Args:
            value (str): The password to validate.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password does not meet the requirements.
        """
        if len(value) < 8:
            logger.warning("Password validation failed: too short.")
            raise ValueError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            logger.warning("Password validation failed: no digits.")
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            logger.warning("Password validation failed: no letters.")
            raise ValueError("Password must contain at least one letter.")
        logger.info("Password validated successfully.")
        return value


class Token(BaseModel):
    """
    Schema for authentication tokens.
    Defines the structure of the token data.
    """

    access_token: str  # The access token string
    token_type: str  # The type of token (e.g., Bearer)


class UserResponse(BaseModel):
    """
    Schema for user response data.
    Defines the structure of user data returned in API responses.
    """

    id: int  # Unique identifier for the user
    email: str  # User's email address
    is_verified: bool  # Indicates if the user's email is verified

    class ConfigDict:
        from_attributes = True  # Allows mapping from ORM models

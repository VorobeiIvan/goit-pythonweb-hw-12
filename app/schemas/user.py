from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
import logging

# Налаштування логування
logger = logging.getLogger(__name__)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))


class UserRole(str, Enum):
    """
    Enumeration of available user roles.
    """

    USER = "user"
    ADMIN = "admin"


class UserBase(BaseModel):
    """
    UserBase schema defines the base structure for user-related data.
    """

    email: EmailStr
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = False
    role: Optional[UserRole] = UserRole.USER

    class ConfigDict:
        from_attributes = True
        arbitrary_types_allowed = True  # Дозволяє кастомні типи


class UserCreate(UserBase):
    """
    UserCreate schema extends UserBase and adds a password field for creating new users.
    """

    password: str

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        """
        Validate the password to ensure it meets security requirements.

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
    Token schema defines the structure for authentication tokens.
    """

    access_token: str
    token_type: str


class UserResponse(BaseModel):
    """
    UserResponse schema defines the structure for user response data.
    """

    id: int
    email: str
    is_verified: bool

    class ConfigDict:
        from_attributes = True

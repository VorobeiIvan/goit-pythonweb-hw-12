from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))  # Виправлено


class UserRole(str):
    """
    Enumeration of available user roles.
    """

    USER = "user"
    ADMIN = "admin"


class UserBase(BaseModel):
    """
    UserBase schema defines the base structure for user-related data.

    Attributes:
        email (EmailStr): The email address of the user. Must be a valid email format.
        is_active (Optional[bool]): Indicates whether the user account is active. Defaults to True.
        is_verified (Optional[bool]): Indicates whether the user's email is verified. Defaults to False.
        role (Optional[str]): The role assigned to the user. Defaults to "user".

    Config:
        orm_mode (bool): Enables compatibility with ORM objects, allowing data to be parsed from ORM models.
    """

    email: EmailStr
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = False
    role: Optional[str] = "user"

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    """
    UserCreate schema extends UserBase and adds a password field for creating new users.

    Attributes:
        password (str): The password for the user.
    """

    password: str


class Token(BaseModel):
    """
    Token schema defines the structure for authentication tokens.

    Attributes:
        access_token (str): The access token string.
        token_type (str): The type of the token (e.g., "bearer").
    """

    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    email: str
    is_verified: bool

    class Config:
        from_attributes = True

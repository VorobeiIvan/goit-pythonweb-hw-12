from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.database.database import Base
from app.models.contacts import Contact


class UserRole(str, enum.Enum):
    """
    Enumeration of available user roles.

    Attributes:
        USER (str): Represents a regular user role.
        ADMIN (str): Represents an admin user role.
    """

    USER = "user"
    ADMIN = "admin"


class User(Base):
    """
    SQLAlchemy model for the User entity.

    Represents a user in the system with attributes such as email, password,
    role, and relationships to other entities like contacts.

    Attributes:
        id (int): Primary key, unique identifier for the user.
        email (str): User's email address, must be unique.
        hashed_password (str): Hashed version of the user's password.
        is_active (bool): Indicates whether the user account is active.
        is_verified (bool): Indicates whether the user's email is verified.
        role (str): User's role in the system (e.g., user or admin).
        contacts (relationship): Relationship to the user's contacts.
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime): Timestamp when the user was last updated.
    """

    __tablename__ = "users"
    __table_args__ = {
        "extend_existing": True
    }  # Ensures table extension if it already exists.

    # Primary key for the user table.
    id = Column(Integer, primary_key=True, index=True)

    # User's email address, must be unique and indexed for fast lookups.
    email = Column(String, unique=True, index=True, nullable=False)

    # Hashed password for secure storage.
    hashed_password = Column(String, nullable=False)

    # Indicates if the user account is active (default is True).
    is_active = Column(Boolean, default=True)

    # Indicates if the user's email is verified (default is False).
    is_verified = Column(Boolean, default=False)

    # Role of the user, defaults to 'user'.
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)

    # Relationship to the Contact model, establishes ownership of contacts.
    contacts = relationship("Contact", back_populates="owner")

    # Timestamp when the user was created, defaults to the current UTC time.
    created_at = Column(DateTime, default=datetime.utcnow)

    # Timestamp when the user was last updated, automatically updated on changes.
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Avoid indexing duplicate attributes in Sphinx documentation.
    """
    :no-index:
    """

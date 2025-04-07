from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.database.database import Base


class UserRole(str, enum.Enum):
    """
    Enumeration of available user roles.
    """

    USER = "user"
    ADMIN = "admin"


class User(Base):
    """
    SQLAlchemy model for User entity.

    Attributes:
        id (int): Primary key
        email (str): User's email address
        hashed_password (str): Hashed password
        is_active (bool): Whether the user is active
        is_verified (bool): Whether the user's email is verified
        role (str): User's role (user/admin)
        contacts (relationship): Relationship to user's contacts
        created_at (datetime): User creation timestamp
        updated_at (datetime): User last update timestamp
    """

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    contacts = relationship("Contact", back_populates="owner")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Avoid indexing duplicate attributes in Sphinx
    """
    :no-index:
    """

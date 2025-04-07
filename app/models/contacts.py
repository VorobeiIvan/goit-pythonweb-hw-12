from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime, date
from app.database.database import Base


class Contact(Base):
    """
    SQLAlchemy model for the Contact entity.

    Represents a contact in the database with attributes such as name, email, phone, birthday,
    and ownership information.

    Attributes:
        id (int): Primary key for the contact.
        first_name (str): The contact's first name.
        last_name (str): The contact's last name.
        email (str): The contact's email address.
        phone (str): The contact's phone number.
        birthday (datetime): The contact's birthday.
        owner_id (int): Foreign key referencing the User who owns this contact.
        owner (relationship): SQLAlchemy relationship to the User entity.
        created_at (datetime): Timestamp when the contact was created.
        updated_at (datetime): Timestamp when the contact was last updated.
    """

    __tablename__ = "contacts"
    __table_args__ = {"extend_existing": True}

    # Primary key for the contact
    id = Column(Integer, primary_key=True, index=True)
    # Contact's first name (required)
    first_name = Column(String(255), nullable=False)
    # Contact's last name (required)
    last_name = Column(String(255), nullable=False)
    # Contact's email address (required)
    email = Column(String(255), nullable=False)
    # Contact's phone number (required)
    phone = Column(String(20), nullable=False)
    # Contact's birthday (required)
    birthday = Column(DateTime, nullable=False)
    # Foreign key to the User entity
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Relationship to the User entity
    owner = relationship("User", back_populates="contacts")
    # Timestamp when the contact was created
    created_at = Column(DateTime, default=datetime.utcnow)
    # Timestamp when the contact was last updated
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ContactCreate(BaseModel):
    """
    Pydantic model for creating a new contact.

    Used for validating and transferring data when creating a new contact.

    Attributes:
        first_name (str): The contact's first name.
        last_name (str): The contact's last name.
        email (EmailStr): The contact's email address (validated as a proper email format).
        phone (str): The contact's phone number.
        birthday (date): The contact's birthday.
        additional_info (Optional[str]): Additional information about the contact (optional).
    """

    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str] = None

    @field_validator("birthday")
    def validate_birthday(cls, value: date) -> date:
        """
        Validate that the birthday is not in the future.

        Ensures that the provided birthday is a valid date and does not exceed the current date.

        Args:
            value (date): The birthday value to validate.

        Returns:
            date: The validated birthday.

        Raises:
            ValueError: If the birthday is in the future.
        """
        if value > date.today():
            raise ValueError("Birthday cannot be in the future.")
        return value

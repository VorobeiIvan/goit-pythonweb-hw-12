from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime, date
from app.database.database import Base


class Contact(Base):
    """
    SQLAlchemy model for Contact entity.

    Attributes:
        id (int): Primary key
        first_name (str): Contact's first name
        last_name (str): Contact's last name
        email (str): Contact's email address
        phone (str): Contact's phone number
        birthday (datetime): Contact's birthday
        owner_id (int): Foreign key to User
        owner (relationship): Relationship to owner User
        created_at (datetime): Contact creation timestamp
        updated_at (datetime): Contact last update timestamp
    """

    __tablename__ = "contacts"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    birthday = Column(DateTime, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="contacts")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ContactCreate(BaseModel):
    """
    Pydantic model for creating a new contact.

    Attributes:
        first_name (str): The contact's first name.
        last_name (str): The contact's last name.
        email (EmailStr): The contact's email address.
        phone (str): The contact's phone number.
        birthday (date): The contact's birthday.
        additional_info (Optional[str]): Additional information about the contact.
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

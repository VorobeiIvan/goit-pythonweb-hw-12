from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr
from typing import Optional
import enum
from datetime import datetime

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

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    birthday = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))
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
        birthday (str): The contact's birthday.
        additional_info (Optional[str]): Additional information about the contact.
    """

    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: str
    additional_info: Optional[str] = None


class ContactResponse(ContactCreate):
    """
    Pydantic model for contact responses.

    Inherits all fields from ContactCreate and adds:
        id (int): The contact's unique identifier.
    """

    id: int

    class Config:
        orm_mode = True

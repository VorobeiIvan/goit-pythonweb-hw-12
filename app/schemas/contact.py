from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import date
import logging

# Налаштування логування
logger = logging.getLogger(__name__)


class ContactCreate(BaseModel):
    """
    ContactCreate is a Pydantic model used for creating a new contact.

    Attributes:
        first_name (str): The first name of the contact. This field is required.
        last_name (str): The last name of the contact. This field is required.
        email (EmailStr): The email address of the contact. Must be a valid email format.
        phone (str): The phone number of the contact. This field is required and should follow a valid phone number format.
        birthday (date): The birthday of the contact. Must be a valid date in the format YYYY-MM-DD.
        additional_info (Optional[str]): Additional information about the contact. This field is optional and can be left empty.
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
            logger.warning(f"Invalid birthday: {value} (in the future)")
            raise ValueError("Birthday cannot be in the future.")
        logger.info(f"Validated birthday: {value}")
        return value

    @field_validator("phone")
    def validate_phone(cls, value: str) -> str:
        """
        Validate the phone number format.

        Args:
            value (str): The phone number to validate.

        Returns:
            str: The validated phone number.

        Raises:
            ValueError: If the phone number format is invalid.
        """
        if not value.isdigit() or len(value) < 7 or len(value) > 15:
            logger.warning(f"Invalid phone number: {value}")
            raise ValueError(
                "Phone number must contain only digits and be 7-15 characters long."
            )
        logger.info(f"Validated phone number: {value}")
        return value


class ContactResponse(ContactCreate):
    """
    ContactResponse is a Pydantic model used for returning contact data.

    Attributes:
        id (int): The unique identifier of the contact.
    """

    id: int

    class ConfigDict:
        from_attributes = True

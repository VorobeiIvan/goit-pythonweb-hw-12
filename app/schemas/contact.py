from pydantic import BaseModel, EmailStr
from typing import Optional


class ContactCreate(BaseModel):
    """
    ContactCreate is a Pydantic model used for creating a new contact.

    Attributes:
        first_name (str): The first name of the contact. This field is required.
        last_name (str): The last name of the contact. This field is required.
        email (EmailStr): The email address of the contact. Must be a valid email format.
        phone (str): The phone number of the contact. This field is required and should follow a valid phone number format.
        birthday (str): The birthday of the contact in string format. It is recommended to use a standard date format (e.g., YYYY-MM-DD).
        additional_info (Optional[str]): Additional information about the contact. This field is optional and can be left empty.

    Notes:
        - This model is designed to validate input data when creating a new contact.
        - Ensure that the `email` field contains a valid email address.
        - The `birthday` field should ideally be validated further to ensure it represents a valid date.
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
    """

    id: int

    class Config:
        orm_mode = True

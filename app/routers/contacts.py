from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.contact import ContactCreate, ContactResponse
from app.models.contacts import Contact
from app.utils.dependencies import get_db, get_current_user
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Create a new contact and associate it with the currently authenticated user.

    Args:
        contact (ContactCreate): The contact data to create.
        db (Session): The database session.
        current_user: The currently authenticated user.

    Returns:
        ContactResponse: The created contact.
    """
    new_contact = Contact(**contact.dict(), owner_id=current_user.id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    logger.info(f"Contact created: {new_contact.id} by user {current_user.id}")
    return new_contact


@router.get("/", response_model=List[ContactResponse], status_code=200)
def get_contacts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve all contacts associated with the currently authenticated user.

    Args:
        db (Session): The database session.
        current_user: The currently authenticated user.

    Returns:
        List[ContactResponse]: A list of contacts.
    """
    contacts = db.query(Contact).filter(Contact.owner_id == current_user.id).all()
    logger.info(f"Retrieved {len(contacts)} contacts for user {current_user.id}")
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, status_code=200)
def get_contact_by_id(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve a specific contact by its ID.

    Args:
        contact_id (int): The ID of the contact to retrieve.
        db (Session): The database session.
        current_user: The currently authenticated user.

    Returns:
        ContactResponse: The contact with the specified ID.

    Raises:
        HTTPException: If the contact is not found.
    """
    contact = (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.owner_id == current_user.id)
        .first()
    )
    if not contact:
        logger.warning(f"Contact {contact_id} not found for user {current_user.id}")
        raise HTTPException(status_code=404, detail="Contact not found")
    logger.info(f"Retrieved contact {contact_id} for user {current_user.id}")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, status_code=200)
def update_contact(
    contact_id: int,
    contact_data: ContactCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update a specific contact by its ID.

    Args:
        contact_id (int): The ID of the contact to update.
        contact_data (ContactCreate): The updated contact data.
        db (Session): The database session.
        current_user: The currently authenticated user.

    Returns:
        ContactResponse: The updated contact.

    Raises:
        HTTPException: If the contact is not found.
    """
    contact = (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.owner_id == current_user.id)
        .first()
    )
    if not contact:
        logger.warning(f"Contact {contact_id} not found for user {current_user.id}")
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact_data.dict().items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    logger.info(f"Contact {contact_id} updated by user {current_user.id}")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse, status_code=200)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete a specific contact by its ID.

    Args:
        contact_id (int): The ID of the contact to delete.
        db (Session): The database session.
        current_user: The currently authenticated user.

    Returns:
        ContactResponse: The deleted contact.

    Raises:
        HTTPException: If the contact is not found.
    """
    contact = (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.owner_id == current_user.id)
        .first()
    )
    if not contact:
        logger.warning(f"Contact {contact_id} not found for user {current_user.id}")
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    logger.info(f"Contact {contact_id} deleted by user {current_user.id}")
    return contact


@router.get("/search", response_model=List[ContactResponse], status_code=200)
def search_contacts(
    query: str = Query(..., description="Search by first name, last name, or email"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Search contacts by first name, last name, or email.

    Args:
        query (str): The search query.
        db (Session): The database session.
        current_user: The currently authenticated user.

    Returns:
        List[ContactResponse]: A list of contacts matching the search query.
    """
    contacts = (
        db.query(Contact)
        .filter(
            Contact.owner_id == current_user.id,
            (Contact.first_name.ilike(f"%{query}%"))
            | (Contact.last_name.ilike(f"%{query}%"))
            | (Contact.email.ilike(f"%{query}%")),
        )
        .all()
    )
    logger.info(
        f"Search query '{query}' returned {len(contacts)} results for user {current_user.id}"
    )
    return contacts


@router.get("/birthdays", response_model=List[ContactResponse], status_code=200)
def get_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get contacts with birthdays in the next 7 days.

    Args:
        db (Session): The database session.
        current_user: The currently authenticated user.

    Returns:
        List[ContactResponse]: A list of contacts with upcoming birthdays.
    """
    today = date.today()
    next_week = today + timedelta(days=7)
    contacts = (
        db.query(Contact)
        .filter(
            Contact.owner_id == current_user.id,
            Contact.birthday.between(today, next_week),
        )
        .all()
    )
    logger.info(
        f"Retrieved {len(contacts)} upcoming birthdays for user {current_user.id}"
    )
    return contacts

from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.contact import ContactCreate, ContactResponse
from app.models.contacts import Contact
from app.utils.dependencies import get_db, get_current_user
import logging

# Налаштування логування
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Creates a new contact and associates it with the currently authenticated user.
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
    Retrieves all contacts associated with the currently authenticated user.
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
    Retrieves a specific contact by its ID.
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
    Updates a specific contact by its ID.
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
    Deletes a specific contact by its ID.
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
    return contacts


@router.get("/birthdays", response_model=List[ContactResponse], status_code=200)
def get_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get contacts with birthdays in the next 7 days.
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
    return contacts

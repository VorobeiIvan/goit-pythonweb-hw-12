from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.contact import ContactCreate, ContactResponse
from app.models.contacts import Contact
from app.utils.dependencies import get_db, get_current_user

router = APIRouter()


@router.post("/", response_model=ContactResponse)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Creates a new contact and associates it with the currently authenticated user.

    Args:
        contact (ContactCreate): The data required to create a new contact.
        db (Session): The database session dependency.
        current_user: The currently authenticated user.

    Returns:
        ContactResponse: The newly created contact object.

    Raises:
        HTTPException: If there is an issue with the database operation.
    """
    new_contact = Contact(**contact.dict(), owner_id=current_user.id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


@router.get("/", response_model=List[ContactResponse])
def get_contacts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieves all contacts associated with the currently authenticated user.

    Args:
        db (Session): The database session dependency.
        current_user: The currently authenticated user.

    Returns:
        List[ContactResponse]: A list of contacts belonging to the user.
    """
    return db.query(Contact).filter(Contact.owner_id == current_user.id).all()


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact_by_id(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieves a specific contact by its ID.

    Args:
        contact_id (int): The ID of the contact to retrieve.
        db (Session): The database session dependency.
        current_user: The currently authenticated user.

    Returns:
        ContactResponse: The contact object.

    Raises:
        HTTPException: If the contact is not found or does not belong to the user.
    """
    contact = (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.owner_id == current_user.id)
        .first()
    )
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact_data: ContactCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Updates a specific contact by its ID.

    Args:
        contact_id (int): The ID of the contact to update.
        contact_data (ContactCreate): The updated contact data.
        db (Session): The database session dependency.
        current_user: The currently authenticated user.

    Returns:
        ContactResponse: The updated contact object.

    Raises:
        HTTPException: If the contact is not found or does not belong to the user.
    """
    contact = (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.owner_id == current_user.id)
        .first()
    )
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact_data.dict().items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Deletes a specific contact by its ID.

    Args:
        contact_id (int): The ID of the contact to delete.
        db (Session): The database session dependency.
        current_user: The currently authenticated user.

    Returns:
        ContactResponse: The deleted contact object.

    Raises:
        HTTPException: If the contact is not found or does not belong to the user.
    """
    contact = (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.owner_id == current_user.id)
        .first()
    )
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return contact

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.services.auth import get_password_hash
from app.utils.dependencies import get_current_user, get_db
from app.utils.dependencies import admin_required
from app.utils.limiter import limiter

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=List[UserResponse], status_code=200)
async def list_users():
    """
    Returns a list of users (placeholder implementation).
    """
    # Placeholder implementation for listing users.
    return []


@router.post("/register/", response_model=UserResponse, status_code=201)
@limiter.limit("5/minute")
def register_user(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user.

    Args:
        request (Request): The HTTP request object.
        user (UserCreate): The user data for registration.
        db (Session): The database session dependency.

    Returns:
        UserResponse: The newly registered user.

    Raises:
        HTTPException: If a user with the same email already exists.
    """
    # Check if the user already exists in the database.
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        logger.warning(f"Registration failed: User {user.email} already exists.")
        raise HTTPException(status_code=409, detail="User already exists")

    # Hash the user's password and create a new user record.
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        is_verified=False,
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User registered successfully: {user.email}")
    return new_user


@router.get("/me/", response_model=UserResponse, status_code=200)
@limiter.limit("10/minute")
def get_current_user_info(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieves the current authenticated user's information.

    Args:
        request (Request): The HTTP request object.
        db (Session): The database session dependency.
        current_user: The currently authenticated user.

    Returns:
        UserResponse: The current user's information.
    """
    # Log and return the current user's information.
    logger.info(f"Retrieved current user info: {current_user.email}")
    return current_user


@router.put("/avatar")
async def update_avatar(avatar_url: str, current_user=Depends(admin_required)):
    """
    Дозволяє адміністраторам змінювати аватар.

    Args:
        avatar_url (str): URL нового аватара.
        current_user: Поточний користувач (перевіряється, чи є він адміністратором).

    Returns:
        dict: Повідомлення про успішну зміну аватара.
    """
    # Логіка зміни аватара
    return {"message": "Avatar updated successfully"}

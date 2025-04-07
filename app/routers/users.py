from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.services.auth import get_password_hash
from app.utils.dependencies import get_current_user, get_db
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
    Повертає список користувачів (заглушка).
    """
    return []


@router.post("/register/", response_model=UserResponse, status_code=201)
@limiter.limit("5/minute")
def register_user(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        logger.warning(f"Registration failed: User {user.email} already exists.")
        raise HTTPException(status_code=409, detail="User already exists")

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
    Get the current authenticated user's information.
    """
    logger.info(f"Retrieved current user info: {current_user.email}")
    return current_user

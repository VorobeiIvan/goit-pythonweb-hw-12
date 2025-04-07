from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import Token
from app.services import redis_cache
from app.utils.security import create_refresh_token, verify_refresh_token
from app.services.auth import authenticate_user, create_access_token
from app.utils.dependencies import get_db
import logging

# Налаштування логування
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/token", response_model=Token, status_code=200)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return an access token and refresh token.
    """
    logger.info(f"Authentication attempt for username: {form_data.username}")
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Authentication failed for username: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    redis_cache.set(f"user:{user.email}", user.id, ex=3600)  # Кешування на 1 годину
    redis_cache.set(
        f"refresh_token:{user.email}", refresh_token, ex=86400
    )  # Кешування refresh токена на 24 години

    logger.info(f"User {user.email} authenticated successfully. Tokens generated.")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/token/refresh", response_model=Token, status_code=200)
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    """
    Refresh the access token using a valid refresh token.
    """
    logger.info("Refresh token attempt.")
    email = verify_refresh_token(refresh_token)
    if not email:
        logger.warning("Invalid refresh token provided.")
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(data={"sub": email})
    logger.info(f"Access token refreshed successfully for user: {email}")
    return {"access_token": access_token, "token_type": "bearer"}

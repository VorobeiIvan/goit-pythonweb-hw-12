from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import Token
from app.services.redis_cache import redis_client
from app.utils.security import create_refresh_token, verify_refresh_token
from app.services.auth import (
    authenticate_user,
    create_access_token,
    verify_password,
    hash_password,
)
from app.utils.dependencies import get_db
from app.models.user import User
from app.services.email import send_password_reset_email
from app.config import settings
import logging
import uuid

# Налаштування логування
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


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
    redis_client.set(f"user:{user.email}", user.id, ex=3600)  # Кешування на 1 годину
    redis_client.set(
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


@router.post("/password-reset-request")
async def password_reset_request(email: str, db: Session = Depends(get_db)):
    """
    Request a password reset by sending a reset link to the user's email.

    Args:
        email (str): The email address of the user requesting the reset.
        db (Session): Database session.

    Returns:
        dict: A success message.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a unique reset token
    reset_token = str(uuid.uuid4())
    redis_client.set(
        f"password_reset:{reset_token}", user.email, ex=3600
    )  # Token valid for 1 hour

    # Send reset email
    reset_url = f"{settings.BASE_URL}/auth/password-reset?token={reset_token}"
    await send_password_reset_email(email, reset_url)

    return {"message": "Password reset link has been sent to your email."}


@router.post("/password-reset")
async def password_reset(token: str, new_password: str, db: Session = Depends(get_db)):
    """
    Reset the user's password using a valid reset token.

    Args:
        token (str): The reset token sent to the user's email.
        new_password (str): The new password for the user.
        db (Session): Database session.

    Returns:
        dict: A success message.
    """
    email = redis_client.get(f"password_reset:{token}")
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    user = db.query(User).filter(User.email == email.decode("utf-8")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user's password
    user.password = hash_password(new_password)
    db.commit()

    # Delete the token from Redis
    redis_client.delete(f"password_reset:{token}")

    return {"message": "Password has been reset successfully."}

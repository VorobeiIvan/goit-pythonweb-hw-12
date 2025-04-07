from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import Token
from app.services.redis_cache import redis_client
from app.utils.security import create_refresh_token, verify_refresh_token
from app.services.auth import (
    authenticate_user,
    create_access_token,
    hash_password,
)
from app.utils.dependencies import get_db
from app.models.user import User
from app.services.email import send_password_reset_email
from app.config import settings
import logging
import uuid


# Configure logging
logger = logging.getLogger(__name__)

# Define the router for authentication-related endpoints
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", response_model=Token, status_code=200)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return an access token and refresh token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing username and password.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary containing the access token, refresh token, and token type.

    Raises:
        HTTPException: If authentication fails due to invalid credentials.
    """
    logger.info(f"Authentication attempt for username: {form_data.username}")
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Authentication failed for username: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate access and refresh tokens
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    # Cache user ID and refresh token in Redis
    redis_client.set(f"user:{user.email}", user.id, ex=3600)  # Cache for 1 hour
    redis_client.set(
        f"refresh_token:{user.email}", refresh_token, ex=86400
    )  # Cache refresh token for 24 hours

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

    Args:
        refresh_token (str): The refresh token provided by the user.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary containing the new access token and token type.

    Raises:
        HTTPException: If the refresh token is invalid or expired.
    """
    logger.info("Refresh token attempt.")
    email = verify_refresh_token(refresh_token)
    if not email:
        logger.warning("Invalid refresh token provided.")
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Generate a new access token
    access_token = create_access_token(data={"sub": email})
    logger.info(f"Access token refreshed successfully for user: {email}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/password-reset-request")
async def password_reset_request(email: str, db: Session = Depends(get_db)):
    """
    Request a password reset by sending a reset link to the user's email.

    Args:
        email (str): The email address of the user requesting the password reset.
        db (Session): The database session dependency.

    Returns:
        dict: A message indicating that the password reset link has been sent.

    Raises:
        HTTPException: If the user with the provided email is not found.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a unique reset token and store it in Redis
    reset_token = str(uuid.uuid4())
    redis_client.set(
        f"password_reset:{reset_token}", user.email, ex=3600
    )  # Token valid for 1 hour

    # Construct the password reset URL and send it via email
    reset_url = f"{settings.BASE_URL}/auth/password-reset?token={reset_token}"
    await send_password_reset_email(email, reset_url)

    return {"message": "Password reset link has been sent to your email."}


@router.post("/password-reset")
async def password_reset(token: str, new_password: str, db: Session = Depends(get_db)):
    """
    Reset the user's password using a valid reset token.

    Args:
        token (str): The password reset token provided by the user.
        new_password (str): The new password to set for the user.
        db (Session): The database session dependency.

    Returns:
        dict: A message indicating that the password has been reset successfully.

    Raises:
        HTTPException: If the reset token is invalid or expired, or if the user is not found.
    """
    # Retrieve the email associated with the reset token from Redis
    email = redis_client.get(f"password_reset:{token}")
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    # Find the user in the database
    user = db.query(User).filter(User.email == email.decode("utf-8")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user's password and commit the changes
    user.password = hash_password(new_password)
    db.commit()

    # Remove the reset token from Redis
    redis_client.delete(f"password_reset:{token}")

    return {"message": "Password has been reset successfully."}

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config import settings
import logging

# Налаштування логування
logger = logging.getLogger(__name__)

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    result = pwd_context.verify(plain_password, hashed_password)
    if result:
        logger.info("Password verification successful.")
    else:
        logger.warning("Password verification failed.")
    return result


def get_password_hash(password: str) -> str:
    """
    Hash a password.
    """
    hashed_password = pwd_context.hash(password)
    logger.info("Password hashed successfully.")
    return hashed_password


def create_access_token(data: dict) -> str:
    """
    Create an access token with a shorter expiration time (e.g. 15 minutes).
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)  # Access токен діє 15 хвилин
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    logger.info("Access token created successfully.")
    return encoded_jwt


def verify_access_token(token: str) -> str:
    """
    Verify the access token and return the email if valid.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            logger.warning("Access token verification failed: no email found.")
            return None
        logger.info("Access token verified successfully.")
        return email
    except JWTError as e:
        logger.error(f"Access token verification failed: {e}")
        return None


def create_refresh_token(data: dict) -> str:
    """
    Create a refresh token with a longer expiration time (1 day).
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=1)  # Refresh токен діє 1 день
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    logger.info("Refresh token created successfully.")
    return encoded_jwt


def verify_refresh_token(token: str) -> str:
    """
    Verify the refresh token and return the email if valid.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            logger.warning("Refresh token verification failed: no email found.")
            return None
        logger.info("Refresh token verified successfully.")
        return email
    except JWTError as e:
        logger.error(f"Refresh token verification failed: {e}")
        return None

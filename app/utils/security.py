from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config import settings
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Initialize the password hashing context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a hashed password.

    Args:
        plain_password (str): The plain-text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Create an access token with a short expiration time (e.g., 15 minutes).

    Args:
        data (dict): The data to encode in the token.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=15
    )  # Access token valid for 15 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    logger.info("Access token created successfully.")
    return encoded_jwt


def verify_access_token(token: str) -> str:
    """
    Verify the access token and extract the email if valid.

    Args:
        token (str): The JWT access token to verify.

    Returns:
        str: The email extracted from the token if valid, None otherwise.
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
    Create a refresh token with a longer expiration time (e.g., 1 day).

    Args:
        data (dict): The data to encode in the token.

    Returns:
        str: The encoded JWT refresh token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=1)  # Refresh token valid for 1 day
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    logger.info("Refresh token created successfully.")
    return encoded_jwt


def verify_refresh_token(token: str) -> str:
    """
    Verify the refresh token and extract the email if valid.

    Args:
        token (str): The JWT refresh token to verify.

    Returns:
        str: The email extracted from the token if valid, None otherwise.
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

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.models.user import User
from sqlalchemy.orm import Session
import os
import logging

# Logging configuration
logger = logging.getLogger(__name__)

# Password hashing configuration using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv(
    "SECRET_KEY", "default_secret_key"
)  # Use the value from .env or a default value
ALGORITHM = "HS256"  # Algorithm used for JWT encoding
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Default token expiration time in minutes


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if a plain text password matches the hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    result = pwd_context.verify(plain_password, hashed_password)
    if result:
        logger.info("Password verification successful.")
    else:
        logger.warning("Password verification failed.")
    return result


def get_password_hash(password: str) -> str:
    """
    Hash a plain text password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    hashed_password = pwd_context.hash(password)
    logger.info("Password hashed successfully.")
    return hashed_password


def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Authenticate a user by verifying their email and password.

    Args:
        db (Session): The database session.
        email (str): The user's email address.
        password (str): The user's plain text password.

    Returns:
        User: The authenticated user object if authentication is successful.
        None: If authentication fails.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning(f"Authentication failed: User with email {email} not found.")
        return None
    if not verify_password(password, user.hashed_password):
        logger.warning(f"Authentication failed: Incorrect password for email {email}.")
        return None
    logger.info(f"User {email} authenticated successfully.")
    return user


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JSON Web Token (JWT) for user authentication.

    Args:
        data (dict): The payload data to include in the token.
        expires_delta (timedelta, optional): The duration for which the token
            will remain valid. Defaults to 30 minutes.

    Returns:
        str: The encoded JWT as a string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info("Access token created successfully.")
    return token


def hash_password(password: str) -> str:
    """
    Hash a plain text password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a refresh token for user authentication.

    Args:
        data (dict): The payload data to include in the token.
        expires_delta (timedelta, optional): The duration for which the token
            will remain valid. Defaults to 7 days.

    Returns:
        str: The encoded JWT as a string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info("Refresh token created successfully.")
    return token

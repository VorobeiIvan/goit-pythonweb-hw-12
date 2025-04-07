from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.models.user import User
from sqlalchemy.orm import Session
import os
import logging

# Налаштування логування
logger = logging.getLogger(__name__)

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv(
    "SECRET_KEY", "default_secret_key"
)  # Використовуйте значення з .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): Plain text password to verify.
        hashed_password (str): Hashed password to verify against.

    Returns:
        bool: True if passwords match, False otherwise.
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

    Args:
        password (str): Plain text password to hash.

    Returns:
        str: Hashed password.
    """
    hashed_password = pwd_context.hash(password)
    logger.info("Password hashed successfully.")
    return hashed_password


def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Authenticate a user with email and password.

    Args:
        db (Session): The database session.
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        User: The authenticated user object if successful, None otherwise.
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
    Generate a JSON Web Token (JWT) for authentication purposes.

    Args:
        data (dict): The payload data to include in the token.
        expires_delta (timedelta, optional): The duration for which the token
            will remain valid. Defaults to 15 minutes.

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

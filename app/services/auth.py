from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.models.user import User
from sqlalchemy.orm import Session

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your_secret_key"  # Замініть на значення з .env
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
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password.

    Args:
        password (str): Plain text password to hash.

    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)


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
    if not user or not verify_password(password, user.hashed_password):
        return None
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
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

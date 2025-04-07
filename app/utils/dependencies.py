import logging
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.database.database import SessionLocal
from app.models.user import User
from app.services.auth import SECRET_KEY, ALGORITHM
from app.services.redis_cache import redis_client  # Import Redis client
import json


# Configure logging
logger = logging.getLogger(__name__)


def get_db():
    """
    Dependency to provide a database session.

    This function creates a new SQLAlchemy database session and ensures
    it is properly closed after use.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str, db: Session = Depends(get_db)) -> User:
    """
    Retrieve the current user based on the provided JWT token, with Redis caching.

    This function decodes the JWT token to extract the user's email, checks if the user
    is cached in Redis, and retrieves the user from the database if not found in the cache.
    The user is then cached in Redis for future requests.

    Args:
        token (str): The JWT token provided by the client for authentication.
        db (Session): A SQLAlchemy database session dependency for querying the database.

    Returns:
        User: The user object corresponding to the email extracted from the token.

    Raises:
        HTTPException: If the token is invalid, expired, or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            logger.warning("Token does not contain a valid email.")
            raise credentials_exception

        # Check if the user is cached in Redis
        cached_user = redis_client.get(email)
        if cached_user:
            logger.info(f"User {email} retrieved from cache.")
            user_data = json.loads(cached_user)
            return User(**user_data)

        # If the user is not in the cache, retrieve them from the database
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            logger.warning(f"User with email {email} not found.")
            raise credentials_exception

        # Cache the user in Redis for 30 minutes
        redis_client.set(email, json.dumps(user.__dict__), ex=1800)
        logger.info(f"User {email} cached successfully.")
        return user
    except JWTError as e:
        # Handle JWT decoding errors
        logger.error(f"JWT decoding error: {e}")
        raise credentials_exception


def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )
    return current_user

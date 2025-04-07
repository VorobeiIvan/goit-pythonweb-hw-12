import logging
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.database.database import SessionLocal
from app.models.user import User
from app.services.auth import SECRET_KEY, ALGORITHM
from app.services.redis_cache import redis_client  # Імпорт клієнта Redis
import json

# Налаштування логування
logger = logging.getLogger(__name__)


def get_db():
    """
    Dependency to get a database session.

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
        # Декодування токена
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            logger.warning("Token does not contain a valid email.")
            raise credentials_exception

        # Перевірка користувача в кеші Redis
        cached_user = redis_client.get(email)
        if cached_user:
            logger.info(f"User {email} retrieved from cache.")
            user_data = json.loads(cached_user)
            return User(**user_data)

        # Якщо користувача немає в кеші, отримуємо його з бази даних
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            logger.warning(f"User with email {email} not found.")
            raise credentials_exception

        # Збереження користувача в кеш Redis
        redis_client.set(
            email, json.dumps(user.__dict__), ex=1800
        )  # Кешування на 30 хвилин
        logger.info(f"User {email} cached successfully.")
        return user
    except JWTError as e:
        logger.error(f"JWT decoding error: {e}")
        raise credentials_exception

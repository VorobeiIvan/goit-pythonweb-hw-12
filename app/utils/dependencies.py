from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.database.database import SessionLocal
from app.models.user import User
from app.services.auth import SECRET_KEY, ALGORITHM


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
    Retrieve the current user based on the provided JWT token.

    This function decodes the JWT token to extract the user's email and fetches
    the corresponding user from the database. If the token is invalid, expired,
    or the user does not exist, an HTTPException with a 401 status code is raised.

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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

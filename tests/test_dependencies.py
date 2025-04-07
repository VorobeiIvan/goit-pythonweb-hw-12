from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.utils.dependencies import get_current_user
from app.models.user import User
import pytest


def test_get_current_user_not_found():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    mock_redis_client = MagicMock()
    mock_redis_client.get.return_value = None

    with patch("app.utils.dependencies.redis_client", mock_redis_client), patch(
        "app.utils.dependencies.jwt.decode", return_value={"sub": "test@example.com"}
    ):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user("mock_token", db=mock_db)
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid token"


def test_get_db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.database.database import Base

    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    generator = override_get_db()
    db = next(generator)
    assert db is not None  # Check that the session is created

    try:
        next(generator)
    except StopIteration:
        pass

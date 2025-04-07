from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.models.user import User
from app.services.auth import get_password_hash
from app.utils.dependencies import get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def setup_test_user():
    db = TestingSessionLocal()
    db.query(User).filter(User.email == "test@example.com").delete()
    db.commit()
    test_user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password"),
        is_active=True,
        is_verified=True,
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    yield test_user
    db.close()

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

# Define the in-memory SQLite database URL for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create a database engine with SQLite in-memory database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session factory for the test database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all database tables in the in-memory database
Base.metadata.create_all(bind=engine)

# Override the `get_db` dependency to use the test database
def override_get_db():
    """
    Dependency override to provide a test database session.
    This ensures that tests use an isolated in-memory database.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply the dependency override to the FastAPI app
app.dependency_overrides[get_db] = override_get_db

# Create a test client for the FastAPI app
client = TestClient(app)

@pytest.fixture
def setup_test_user():
    """
    Pytest fixture to set up a test user in the database.
    This fixture creates a user with predefined credentials and cleans up after the test.
    """
    db = TestingSessionLocal()
    # Remove any existing user with the same email to ensure a clean state
    db.query(User).filter(User.email == "test@example.com").delete()
    db.commit()
    
    # Create a test user with hashed password and active/verified status
    test_user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password"),
        is_active=True,
        is_verified=True,
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    
    # Yield the test user for use in tests
    yield test_user
    
    # Close the database session after the test
    db.close()

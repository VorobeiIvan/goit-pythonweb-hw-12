import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from app.database.database import Base
from app.models.contacts import Contact
from app.utils.dependencies import get_db
from main import app

# Define the in-memory SQLite database URL for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create a database engine with SQLite in-memory database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session factory for the testing database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all database tables based on the models
Base.metadata.create_all(bind=engine)

# Override the dependency to use the testing database session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Replace the default database dependency with the testing one
app.dependency_overrides[get_db] = override_get_db

# Initialize the FastAPI test client
client = TestClient(app)

# Pytest fixture to set up test data in the database
@pytest.fixture
def setup_test_data():
    """
    Fixture to populate the in-memory database with test data.
    Creates two sample contacts for testing purposes.
    """
    db = TestingSessionLocal()
    contact_1 = Contact(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        birthday=date(1990, 5, 15),
        owner_id=1,  # Added owner_id for testing ownership
    )
    contact_2 = Contact(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        phone="9876543210",
        birthday=date(1992, 8, 25),
        owner_id=1,  # Added owner_id for testing ownership
    )
    # Add the contacts to the database
    db.add(contact_1)
    db.add(contact_2)
    db.commit()
    # Refresh the objects to retrieve updated data from the database
    db.refresh(contact_1)
    db.refresh(contact_2)
    db.close()

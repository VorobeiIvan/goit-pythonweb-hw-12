import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from app.database.database import Base
from app.models.contacts import Contact
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
def setup_test_data():
    db = TestingSessionLocal()
    contact_1 = Contact(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        birthday=date(1990, 5, 15),
        owner_id=1,  # Додано owner_id
    )
    contact_2 = Contact(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        phone="9876543210",
        birthday=date(1992, 8, 25),
        owner_id=1,  # Додано owner_id
    )
    db.add(contact_1)
    db.add(contact_2)
    db.commit()
    db.refresh(contact_1)
    db.refresh(contact_2)
    db.close()

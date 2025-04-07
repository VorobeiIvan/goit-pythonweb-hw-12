from app.database.database import Base
from fastapi.testclient import TestClient
from app.utils.dependencies import get_db
from main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Створення SQLite бази даних у пам'яті
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Створення таблиць у базі даних
Base.metadata.create_all(bind=engine)


# Перевизначення залежності get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# Фікстура для клієнта тестування
@pytest.fixture
def client():
    return TestClient(app)

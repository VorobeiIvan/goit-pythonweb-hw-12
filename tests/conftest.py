import sys
import os

# Додаємо кореневу папку проекту до sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Приклад фікстури для бази даних
import pytest
from app.database.database import SessionLocal, Base, engine


@pytest.fixture(scope="function")
def db_session():
    """
    Фікстура для створення тестової сесії бази даних.
    """
    Base.metadata.create_all(bind=engine)  # Створення таблиць
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)  # Видалення таблиць після тесту

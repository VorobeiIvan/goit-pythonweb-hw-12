import pytest
from sqlalchemy.exc import OperationalError
from app.database.database import engine, SessionLocal


def test_database_connection():
    """
    Тест для перевірки підключення до бази даних.
    """
    try:
        # Перевіряємо, чи можна виконати підключення до бази даних
        connection = engine.connect()
        connection.close()
    except OperationalError as e:
        pytest.fail(f"Database connection failed: {e}")


def test_database_session():
    """
    Тест для перевірки створення сесії бази даних.
    """
    try:
        # Перевіряємо, чи можна створити сесію
        session = SessionLocal()
        session.execute("SELECT 1")  # Виконуємо простий запит
        session.close()
    except Exception as e:
        pytest.fail(f"Database session creation failed: {e}")

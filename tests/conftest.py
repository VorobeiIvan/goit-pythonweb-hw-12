from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.utils.dependencies import get_db
from app.models.user import User
from main import app
import pytest

# Створення тестової бази даних SQLite у пам'яті
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Створення таблиць у тестовій базі
Base.metadata.create_all(bind=engine)


# Перевизначення залежності get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Перевизначення залежностей FastAPI
app.dependency_overrides[get_db] = override_get_db


# Фікстура для очищення бази даних перед кожним тестом
@pytest.fixture(scope="function", autouse=True)
def setup_test_database():
    # Очищення таблиць перед кожним тестом
    Base.metadata.drop_all(bind=engine)  # Видалення таблиць
    Base.metadata.create_all(bind=engine)  # Заново створення таблиць


from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print("Таблиці в базі даних:", tables)

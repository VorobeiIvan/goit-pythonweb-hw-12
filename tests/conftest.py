from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.utils.dependencies import get_db
from app.models.user import User
from main import app
import pytest

# Create a test SQLite database in memory
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the test database
Base.metadata.create_all(bind=engine)


# Override the get_db dependency to use the test database
def override_get_db():
    """
    Provides a database session for testing purposes.
    Ensures that the test database is used instead of the production database.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override FastAPI dependencies
app.dependency_overrides[get_db] = override_get_db


# Fixture to reset the database before each test
@pytest.fixture(scope="function", autouse=True)
def setup_test_database():
    """
    Resets the database by dropping and recreating all tables before each test.
    Ensures a clean state for every test case.
    """
    # Drop all tables before each test
    Base.metadata.drop_all(bind=engine)
    # Recreate all tables before each test
    Base.metadata.create_all(bind=engine)


# Inspect the database and print the list of tables
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables in the database:", tables)

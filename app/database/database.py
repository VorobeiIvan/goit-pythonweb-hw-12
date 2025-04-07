import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

# Налаштування логування
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.error("DATABASE_URL is not set in the environment variables.")
    raise ValueError("DATABASE_URL is not set in the environment variables.")


def get_engine():
    """
    Create and return a SQLAlchemy engine based on the DATABASE_URL.

    Returns:
        Engine: SQLAlchemy engine instance.

    Raises:
        Exception: If the engine creation fails.
    """
    try:
        if DATABASE_URL.startswith("sqlite://"):
            logger.info("Using SQLite database.")
            return create_engine(
                DATABASE_URL,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
        logger.info("Using non-SQLite database.")
        return create_engine(DATABASE_URL)
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        raise


# Ініціалізація бази даних
try:
    engine = get_engine()
    logger.info("Database engine created successfully.")
except Exception as e:
    logger.critical(f"Failed to initialize database engine: {e}")
    raise

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

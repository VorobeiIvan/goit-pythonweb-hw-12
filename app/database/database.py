import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Retrieve the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Check if DATABASE_URL is set, otherwise raise an error
if not DATABASE_URL:
    logger.error("DATABASE_URL is not set in the environment variables.")
    raise ValueError("DATABASE_URL is not set in the environment variables.")


def get_engine():
    """
    Create and return a SQLAlchemy engine based on the DATABASE_URL.

    If the database URL points to a SQLite database, additional configurations
    are applied to ensure compatibility.

    Returns:
        sqlalchemy.engine.Engine: SQLAlchemy engine instance.

    Raises:
        Exception: If the engine creation fails.
    """
    try:
        if DATABASE_URL.startswith("sqlite://"):
            # Special configuration for SQLite databases
            logger.info("Using SQLite database.")
            return create_engine(
                DATABASE_URL,
                connect_args={"check_same_thread": False},  # Required for SQLite
                poolclass=StaticPool,  # Use a static pool for SQLite
            )
        # Configuration for non-SQLite databases
        logger.info("Using non-SQLite database.")
        return create_engine(DATABASE_URL)
    except Exception as e:
        # Log and re-raise any exceptions during engine creation
        logger.error(f"Failed to create database engine: {e}")
        raise


# Initialize the database engine
try:
    engine = get_engine()
    logger.info("Database engine created successfully.")
except Exception as e:
    # Log critical errors and terminate if the engine cannot be created
    logger.critical(f"Failed to initialize database engine: {e}")
    raise

# Base class for SQLAlchemy ORM models
Base = declarative_base()

# Session factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

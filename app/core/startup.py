from app.database.database import Base, engine
import logging

# Configure logger for this module
logger = logging.getLogger(__name__)


def initialize_database():
    """
    Initialize the database by creating all tables defined in the SQLAlchemy models.

    This function uses the SQLAlchemy `Base.metadata.create_all` method to create
    all tables in the database that are defined in the models. It logs the process
    and raises an exception if table creation fails.

    Raises:
        Exception: If table creation fails, the exception is logged and re-raised.
    """
    try:
        # Log the start of the table creation process
        logger.info("Creating database tables...")

        # Create all tables defined in the SQLAlchemy models
        Base.metadata.create_all(bind=engine)

        # Log success message
        logger.info("Database tables created successfully.")
    except Exception as e:
        # Log the error and re-raise the exception
        logger.error(f"Failed to create database tables: {e}")
        raise

from app.database.database import Base, engine
import logging

logger = logging.getLogger(__name__)


def initialize_database():
    """
    Initialize the database by creating all tables defined in the models.

    Raises:
        Exception: If table creation fails.
    """
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

from fastapi import FastAPI
from app.routers import auth, contacts, users
import logging

# Налаштування логування
logger = logging.getLogger(__name__)


def add_routers(app: FastAPI):
    """
    Add all routers to the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    logger.info("Adding authentication router...")
    app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
    logger.info("Authentication router added successfully.")

    logger.info("Adding contacts router...")
    app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
    logger.info("Contacts router added successfully.")

    logger.info("Adding users router...")
    app.include_router(users.router, prefix="/users", tags=["Users"])
    logger.info("Users router added successfully.")

from fastapi import FastAPI
from app.routers import auth, contacts, users
import logging

# Configure logging for the module
logger = logging.getLogger(__name__)


def add_routers(app: FastAPI):
    """
    Add all routers to the FastAPI application.

    This function registers the routers for authentication, contacts,
    and users with the provided FastAPI application instance. Each router
    is assigned a specific prefix and tag for better organization.

    Args:
        app (FastAPI): The FastAPI application instance to which the routers will be added.
    """
    # Add the authentication router
    logger.info("Adding authentication router...")
    app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
    logger.info("Authentication router added successfully.")

    # Add the contacts router
    logger.info("Adding contacts router...")
    app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
    logger.info("Contacts router added successfully.")

    # Add the users router
    logger.info("Adding users router...")
    app.include_router(users.router, prefix="/users", tags=["Users"])
    logger.info("Users router added successfully.")

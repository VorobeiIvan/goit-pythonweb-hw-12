from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from app.utils.limiter import limiter
import logging

# Configure logging for the middleware module
logger = logging.getLogger(__name__)


def add_middlewares(app: FastAPI):
    """
    Add all necessary middleware to the FastAPI application.

    This function configures and adds middleware to the FastAPI application instance.
    It includes:
    - CORS middleware to handle Cross-Origin Resource Sharing.
    - SlowAPI middleware for rate limiting.

    Args:
        app (FastAPI): The FastAPI application instance to which middleware will be added.
    """
    # Add CORS middleware to allow cross-origin requests
    logger.info("Adding CORS middleware...")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow requests from all origins
        allow_credentials=True,  # Allow cookies to be included in requests
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )
    logger.info("CORS middleware added successfully.")

    # Add SlowAPI middleware for rate limiting
    logger.info("Adding SlowAPI middleware...")
    app.state.limiter = limiter  # Attach the rate limiter instance to the app state
    app.add_middleware(SlowAPIMiddleware)
    logger.info("SlowAPI middleware added successfully.")

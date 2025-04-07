from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from app.utils.limiter import limiter
import logging

# Налаштування логування
logger = logging.getLogger(__name__)


def add_middlewares(app: FastAPI):
    """
    Add all necessary middleware to the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    logger.info("Adding CORS middleware...")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS middleware added successfully.")

    logger.info("Adding SlowAPI middleware...")
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)
    logger.info("SlowAPI middleware added successfully.")

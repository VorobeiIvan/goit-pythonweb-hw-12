from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.middleware import add_middlewares
from app.core.exception_handlers import add_exception_handlers
from app.core.routers import add_routers
from app.core.startup import initialize_database
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create a lifespan manager for the FastAPI application
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.

    This function is called when the application starts and stops.
    It initializes the database and logs the application lifecycle events.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    logger.info("Starting application...")
    initialize_database()  # Initialize the database connection or setup
    logger.info("Application started successfully.")
    yield
    logger.info(
        "Shutting down application..."
    )  # Log when the application is shutting down


# Initialize FastAPI application with the lifespan manager
app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the application is running.

    This endpoint can be used to check the status of the application.

    Returns:
        dict: A dictionary with the status of the application.
    """
    logger.info("Health check endpoint called.")
    return {"status": "ok"}


# Add middlewares to the application
add_middlewares(app)

# Add custom exception handlers to the application
add_exception_handlers(app)

# Add routers (endpoints) to the application
add_routers(app)

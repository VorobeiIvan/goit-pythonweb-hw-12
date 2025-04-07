from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.middleware import add_middlewares
from app.core.exception_handlers import add_exception_handlers
from app.core.routers import add_routers
from app.core.startup import initialize_database
import logging

# Ініціалізація логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Створення Lifespan менеджера
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    initialize_database()
    logger.info("Application started successfully.")
    yield
    logger.info(
        "Shutting down application..."
    )  # Логування при завершенні роботи додатка


# Ініціалізація FastAPI з Lifespan
app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the application is running.

    Returns:
        dict: A dictionary with the status of the application.
    """
    logger.info("Health check endpoint called.")
    return {"status": "ok"}


# Виклик функцій
add_middlewares(app)
add_exception_handlers(app)
add_routers(app)

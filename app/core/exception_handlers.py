from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import logging

# Налаштування логування
logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI):
    """
    Add custom exception handlers to the FastAPI application.
    """

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
        """
        Handle RateLimitExceeded exceptions.
        """
        logger.warning(f"Rate limit exceeded for request: {request.url}")
        # Динамічне повідомлення: exc.error_message або str(exc)
        message = getattr(exc, "error_message", None) or str(exc)
        return JSONResponse(
            status_code=429,
            content={"detail": message},
        )

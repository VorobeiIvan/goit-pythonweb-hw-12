from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import logging

# Configure logging
logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI):
    """
    Add custom exception handlers to the FastAPI application.

    This function registers custom exception handlers for specific exceptions
    that may occur during the application's runtime. It ensures that these
    exceptions are handled gracefully and appropriate responses are returned
    to the client.
    """

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
        """
        Handle RateLimitExceeded exceptions.

        This handler is triggered when a request exceeds the rate limit defined
        by the application. It logs a warning and returns a JSON response with
        a 429 status code (Too Many Requests).

        Args:
            request (Request): The incoming HTTP request.
            exc (RateLimitExceeded): The exception raised when the rate limit is exceeded.

        Returns:
            JSONResponse: A response with a 429 status code and a message indicating
            the rate limit has been exceeded.
        """
        # Log a warning with the URL of the request that exceeded the rate limit
        logger.warning(f"Rate limit exceeded for request: {request.url}")

        # Dynamic error message: Use `exc.error_message` if available, otherwise use `str(exc)`
        message = getattr(exc, "error_message", None) or str(exc)

        # Return a JSON response with the error details
        return JSONResponse(
            status_code=429,
            content={"detail": message},
        )

from fastapi import FastAPI
from fastapi.testclient import TestClient
from slowapi.errors import RateLimitExceeded
from app.core.exception_handlers import add_exception_handlers


class MockLimit:
    """
    Mock class to simulate the Limit object used in RateLimitExceeded.
    This is used to provide a custom error message for testing purposes.
    """

    def __init__(self, error_message):
        self.error_message = error_message


def test_rate_limit_exceeded_handler():
    """
    Test the custom exception handler for the RateLimitExceeded exception.
    This ensures that the application correctly handles rate-limiting errors.
    """
    # Create a test FastAPI application
    app = FastAPI()

    # Add custom exception handlers to the application
    add_exception_handlers(app)

    # Define a test route that raises the RateLimitExceeded exception
    @app.get("/test-rate-limit")
    async def test_route():
        # Simulate a rate limit exceeded error
        raise RateLimitExceeded(MockLimit("Rate limit exceeded for this endpoint."))

    # Create a test client for the application
    client = TestClient(app)

    # Call the test route and verify the response
    response = client.get("/test-rate-limit")
    
    # Assert that the response status code is 429 (Too Many Requests)
    assert response.status_code == 429
    
    # Assert that the response contains the expected error message
    assert "Rate limit exceeded for this endpoint." in response.json()["detail"]

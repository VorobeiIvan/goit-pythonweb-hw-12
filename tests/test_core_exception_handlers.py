from fastapi import FastAPI
from fastapi.testclient import TestClient
from slowapi.errors import RateLimitExceeded
from app.core.exception_handlers import add_exception_handlers


class MockLimit:
    """
    Мок-клас для імітації об'єкта Limit, який використовується в RateLimitExceeded.
    """

    def __init__(self, error_message):
        self.error_message = error_message


def test_rate_limit_exceeded_handler():
    """
    Test the custom exception handler for RateLimitExceeded.
    """
    # Створюємо тестовий додаток FastAPI
    app = FastAPI()

    # Додаємо обробник виключень
    add_exception_handlers(app)

    # Створюємо тестовий маршрут, який викликає RateLimitExceeded
    @app.get("/test-rate-limit")
    async def test_route():
        raise RateLimitExceeded(MockLimit("Rate limit exceeded for this endpoint."))

    # Створюємо клієнт для тестування
    client = TestClient(app)

    # Викликаємо маршрут і перевіряємо відповідь
    response = client.get("/test-rate-limit")
    assert response.status_code == 429
    assert "Rate limit exceeded for this endpoint." in response.json()["detail"]

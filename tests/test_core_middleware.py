from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from app.core.middleware import add_middlewares


def test_add_cors_middleware():
    """
    Test that CORS middleware is added to the FastAPI application.
    """
    app = FastAPI()
    add_middlewares(app)

    # Перевіряємо, чи додано CORS middleware
    cors_middleware = next(
        (
            middleware
            for middleware in app.user_middleware
            if middleware.cls is CORSMiddleware
        ),
        None,
    )
    assert cors_middleware is not None, "CORS middleware was not added."


def test_add_slowapi_middleware():
    """
    Test that SlowAPI middleware is added to the FastAPI application.
    """
    app = FastAPI()
    add_middlewares(app)

    # Перевіряємо, чи додано SlowAPI middleware
    slowapi_middleware = next(
        (
            middleware
            for middleware in app.user_middleware
            if middleware.cls is SlowAPIMiddleware
        ),
        None,
    )
    assert slowapi_middleware is not None, "SlowAPI middleware was not added."


def test_limiter_state():
    """
    Test that the limiter is set in the application state.
    """
    app = FastAPI()
    add_middlewares(app)

    # Перевіряємо, чи встановлено limiter у стані додатка
    assert hasattr(
        app.state, "limiter"
    ), "Limiter was not set in the application state."
    assert app.state.limiter is not None, "Limiter is None in the application state."

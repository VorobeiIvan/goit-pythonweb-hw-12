import pytest
from app.services.auth import create_access_token, verify_access_token
from datetime import timedelta
from jose import JWTError


@pytest.fixture
def secret_key():
    """
    Фікстура для секретного ключа.
    """
    return "test_secret_key"


@pytest.fixture
def algorithm():
    """
    Фікстура для алгоритму шифрування.
    """
    return "HS256"


@pytest.fixture
def test_user_email():
    """
    Фікстура для тестового email користувача.
    """
    return "test@example.com"


def test_create_access_token(secret_key, algorithm, test_user_email):
    """
    Тест для перевірки створення JWT токена.
    """
    token = create_access_token(
        data={"sub": test_user_email},
        secret_key=secret_key,
        algorithm=algorithm,
        expires_delta=timedelta(minutes=15),
    )
    assert token is not None, "Access token was not created"
    assert isinstance(token, str), "Access token should be a string"


def test_verify_access_token(secret_key, algorithm, test_user_email):
    """
    Тест для перевірки валідації JWT токена.
    """
    # Створюємо токен
    token = create_access_token(
        data={"sub": test_user_email},
        secret_key=secret_key,
        algorithm=algorithm,
        expires_delta=timedelta(minutes=15),
    )

    # Перевіряємо токен
    payload = verify_access_token(token, secret_key=secret_key, algorithm=algorithm)
    assert payload is not None, "Payload should not be None"
    assert payload.get("sub") == test_user_email, "Email in payload does not match"


def test_verify_access_token_invalid(secret_key, algorithm):
    """
    Тест для перевірки валідації невалідного JWT токена.
    """
    invalid_token = "invalid.token.value"
    with pytest.raises(JWTError):
        verify_access_token(invalid_token, secret_key=secret_key, algorithm=algorithm)

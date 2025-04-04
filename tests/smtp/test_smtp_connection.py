import os
import smtplib
import pytest


@pytest.fixture
def smtp_settings():
    """
    Фікстура для отримання налаштувань SMTP із змінних середовища.
    """
    return {
        "server": os.getenv("SMTP_SERVER", "localhost"),
        "port": int(os.getenv("SMTP_PORT", 1025)),
        "email": os.getenv("SMTP_EMAIL", "test@example.com"),
        "password": os.getenv("SMTP_PASSWORD", "password"),
    }


def test_smtp_connection(smtp_settings):
    """
    Тест для перевірки підключення до SMTP-сервера.
    """
    try:
        with smtplib.SMTP(smtp_settings["server"], smtp_settings["port"]) as smtp:
            smtp.noop()  # Перевірка доступності сервера
    except Exception as e:
        pytest.fail(f"Failed to connect to SMTP server: {e}")


def test_smtp_authentication(smtp_settings):
    """
    Тест для перевірки аутентифікації на SMTP-сервері.
    """
    try:
        with smtplib.SMTP(smtp_settings["server"], smtp_settings["port"]) as smtp:
            smtp.starttls()  # Початок TLS-з'єднання
            smtp.login(
                smtp_settings["email"], smtp_settings["password"]
            )  # Аутентифікація
    except smtplib.SMTPAuthenticationError:
        pytest.fail("SMTP authentication failed")
    except Exception as e:
        pytest.fail(f"Failed to authenticate with SMTP server: {e}")

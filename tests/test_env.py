import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import smtplib
import redis

# Load environment variables from the .env file
load_dotenv()


def test_env_variables_exist():
    """
    Test if all required environment variables are loaded.
    Ensures that critical environment variables are present in the .env file.
    """
    required_variables = [
        "SECRET_KEY",
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "DATABASE_URL",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_SERVER",
        "POSTGRES_PORT",
        "POSTGRES_DB",
        "ALGORITHM",
        "SMTP_SERVER",
        "SMTP_PORT",
        "SMTP_EMAIL",
        "SMTP_PASSWORD",
        "CLOUDINARY_CLOUD_NAME",
        "CLOUDINARY_API_KEY",
        "CLOUDINARY_API_SECRET",
        "REDIS_HOST",
        "REDIS_PORT",
    ]

    for var in required_variables:
        # Assert that each required variable is not None
        assert os.getenv(var) is not None, f"{var} is missing in .env"


def test_env_variable_formats():
    """
    Test if environment variables have correct formats.
    Validates specific environment variables for proper formatting and data types.
    """
    # Validate DATABASE_URL format
    database_url = os.getenv("DATABASE_URL")
    assert database_url and database_url.startswith(
        "postgresql://"
    ), "DATABASE_URL must start with 'postgresql://'"

    # Validate SMTP_PORT is a number
    smtp_port = os.getenv("SMTP_PORT")
    assert smtp_port and smtp_port.isdigit(), "SMTP_PORT must be a number"

    # Validate REDIS_PORT is a number
    redis_port = os.getenv("REDIS_PORT")
    assert redis_port and redis_port.isdigit(), "REDIS_PORT must be a number"

    # Validate CLOUDINARY_API_KEY is a number
    cloudinary_api_key = os.getenv("CLOUDINARY_API_KEY")
    assert (
        cloudinary_api_key and cloudinary_api_key.isdigit()
    ), "CLOUDINARY_API_KEY must be a number"


def test_database_connection():
    """
    Test if the application can connect to the database using a test SQLite database.
    """
    database_url = "sqlite:///./test.db"  # Використання SQLite
    try:
        engine = create_engine(database_url, connect_args={"check_same_thread": False})
        connection = engine.connect()
        assert connection is not None, "Failed to connect to the SQLite database"
        connection.close()
    except Exception as e:
        assert False, f"Database connection test failed: {e}"


def test_smtp_connection():
    """
    Test if the application can connect to the SMTP server.
    Ensures that the SMTP server credentials and connection are valid.
    """
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    assert smtp_server, "SMTP_SERVER is not set in the environment variables"
    assert smtp_port and smtp_port.isdigit(), "SMTP_PORT is not set or invalid"
    assert smtp_email, "SMTP_EMAIL is not set in the environment variables"
    assert smtp_password, "SMTP_PASSWORD is not set in the environment variables"

    try:
        # Attempt to connect to the SMTP server
        server = smtplib.SMTP(smtp_server, int(smtp_port))
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.quit()
    except Exception as e:
        assert False, f"Failed to connect to SMTP server: {e}"


def test_redis_connection():
    """
    Test if the application can connect to the Redis server.
    """
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = os.getenv("REDIS_PORT", "6379")

    try:
        client = redis.StrictRedis(
            host=redis_host, port=int(redis_port), decode_responses=True
        )
        assert client.ping(), "Failed to connect to Redis server"
    except Exception as e:
        assert False, f"Failed to connect to Redis server: {e}"

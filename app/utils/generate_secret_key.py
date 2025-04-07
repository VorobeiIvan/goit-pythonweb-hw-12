import secrets
import logging

# Configure logging settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_secret_key() -> str:
    """
    Generate a secure, random, and unique secret key.

    This function uses Python's `secrets` module to generate a cryptographically secure,
    URL-safe random string. The generated key is suitable for use as a SECRET_KEY in
    web applications, ensuring strong security against attacks.

    Returns:
        str: A randomly generated secret key.

    Example usage:
        >>> secret_key = generate_secret_key()
        >>> print(secret_key)
    """
    # Generate a secure, random, URL-safe string of 32 characters
    return secrets.token_urlsafe(32)


if __name__ == "__main__":
    # Log a message to indicate the purpose of the script
    logger.info("Generating a new SECRET_KEY...")

    # Generate the secret key
    secret_key = generate_secret_key()

    # Log and print the generated secret key
    logger.info("Your generated SECRET_KEY:")
    print(secret_key)

    # Provide instructions for the user to use the generated key
    logger.info(
        "Copy the above SECRET_KEY and paste it into your `.env` file under the variable `SECRET_KEY`."
    )

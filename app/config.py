from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration settings.

    Attributes:
        SECRET_KEY (str): Secret key for JWT encoding/decoding.
        ALGORITHM (str): Algorithm used for JWT (default: HS256).
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Expiration time for access tokens in minutes.
    """

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class ConfigDict:
        env_file = (
            ".env"  # Specify that environment variables are loaded from the .env file
        )


# Create a settings instance to be used throughout the application
settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration settings.

    This class is used to manage application settings and load them from
    environment variables or a `.env` file.

    Attributes:
        SECRET_KEY (str): A secret key used for encoding and decoding JWT tokens.
        ALGORITHM (str): The algorithm used for JWT encoding/decoding (default: HS256).
        ACCESS_TOKEN_EXPIRE_MINUTES (int): The expiration time for access tokens in minutes (default: 30).
    """

    # Secret key for JWT encoding/decoding, must be set in the environment or .env file
    SECRET_KEY: str  #: :no-index:

    # Algorithm used for JWT encoding/decoding, default is HS256
    ALGORITHM: str = "HS256"  #: :no-index:

    # Access token expiration time in minutes, default is 30 minutes
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  #: :no-index:

    class ConfigDict:
        # Specify that environment variables are loaded from the .env file
        env_file = ".env"


# Create a settings instance to be used throughout the application
settings = Settings()

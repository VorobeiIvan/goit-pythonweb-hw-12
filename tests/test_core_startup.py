from unittest.mock import MagicMock, patch
from app.core.startup import initialize_database


def test_initialize_database_success():
    """
    Test case: Verifies that the database tables are created successfully.
    Mocks the metadata and engine objects to simulate the database initialization process.
    """
    # Create mock objects for metadata and engine
    mock_metadata = MagicMock()
    mock_engine = MagicMock()

    # Patch the Base.metadata and engine to use the mock objects
    with patch("app.core.startup.Base.metadata", mock_metadata), patch(
        "app.core.startup.engine", mock_engine
    ):
        # Call the function to initialize the database
        initialize_database()

        # Assert that the create_all method was called once with the mock engine
        mock_metadata.create_all.assert_called_once_with(bind=mock_engine)


def test_initialize_database_failure():
    """
    Test case: Ensures that an exception is logged if table creation fails.
    Simulates a failure scenario by raising an exception in the create_all method.
    """
    # Create a mock object for metadata and simulate an exception during table creation
    mock_metadata = MagicMock()
    mock_metadata.create_all.side_effect = Exception("Database error")
    mock_engine = MagicMock()

    # Patch the Base.metadata, engine, and logger to use mock objects
    with patch("app.core.startup.Base.metadata", mock_metadata), patch(
        "app.core.startup.engine", mock_engine
    ), patch("app.core.startup.logger") as mock_logger:
        try:
            # Call the function to initialize the database
            initialize_database()
        except Exception:
            # Suppress the exception to allow further assertions
            pass

        # Assert that the create_all method was called once with the mock engine
        mock_metadata.create_all.assert_called_once_with(bind=mock_engine)

        # Assert that the error message was logged with the expected content
        mock_logger.error.assert_called_once_with(
            "Failed to create database tables: Database error"
        )

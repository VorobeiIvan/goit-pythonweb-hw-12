from unittest.mock import MagicMock, patch
from app.core.startup import initialize_database


def test_initialize_database_success():
    """
    Test that the database tables are created successfully.
    """
    mock_metadata = MagicMock()
    mock_engine = MagicMock()

    with patch("app.core.startup.Base.metadata", mock_metadata), patch(
        "app.core.startup.engine", mock_engine
    ):
        initialize_database()
        mock_metadata.create_all.assert_called_once_with(bind=mock_engine)


def test_initialize_database_failure():
    """
    Test that an exception is logged if table creation fails.
    """
    mock_metadata = MagicMock()
    mock_metadata.create_all.side_effect = Exception("Database error")
    mock_engine = MagicMock()

    with patch("app.core.startup.Base.metadata", mock_metadata), patch(
        "app.core.startup.engine", mock_engine
    ), patch("app.core.startup.logger") as mock_logger:
        try:
            initialize_database()
        except Exception:
            pass
        mock_metadata.create_all.assert_called_once_with(bind=mock_engine)
        mock_logger.error.assert_called_once_with(
            "Failed to create database tables: Database error"
        )

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)


def test_search_contacts():
    with patch("app.utils.dependencies.get_db") as mock_db:
        mock_db.return_value.query.return_value.filter.return_value.all.return_value = [
            MagicMock(first_name="John", last_name="Doe", email="john.doe@example.com")
        ]
        response = client.get("/contacts/search", params={"query": "John"})
        assert response.status_code == 200
        assert len(response.json()) > 0


def test_get_upcoming_birthdays():
    with patch("app.utils.dependencies.get_db") as mock_db:
        mock_db.return_value.query.return_value.filter.return_value.all.return_value = [
            MagicMock(first_name="Jane", last_name="Doe", email="jane.doe@example.com")
        ]
        response = client.get("/contacts/birthdays")
        assert response.status_code == 200
        assert len(response.json()) > 0

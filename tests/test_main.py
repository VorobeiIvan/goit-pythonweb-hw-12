from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """
    Тест для перевірки кореневого маршруту.
    """
    response = client.get("/")
    assert response.status_code == 200, "Root endpoint did not return status 200"
    assert response.json() == {
        "message": "Welcome to the FastAPI Contacts Management API"
    }, "Unexpected response content"


def test_docs_swagger_ui():
    """
    Тест для перевірки доступності Swagger UI.
    """
    response = client.get("/docs")
    assert response.status_code == 200, "Swagger UI is not accessible"
    assert "Swagger UI" in response.text, "Swagger UI page content is missing"


def test_docs_redoc():
    """
    Тест для перевірки доступності ReDoc.
    """
    response = client.get("/redoc")
    assert response.status_code == 200, "ReDoc is not accessible"
    assert "ReDoc" in response.text, "ReDoc page content is missing"

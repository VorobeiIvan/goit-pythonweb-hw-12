from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_swagger_ui():
    """
    Тест для перевірки доступності Swagger UI.
    """
    response = client.get("/docs")
    assert response.status_code == 200, "Swagger UI is not accessible"
    assert "Swagger UI" in response.text, "Swagger UI page content is missing"


def test_redoc():
    """
    Тест для перевірки доступності ReDoc.
    """
    response = client.get("/redoc")
    assert response.status_code == 200, "ReDoc is not accessible"
    assert "ReDoc" in response.text, "ReDoc page content is missing"


def test_openapi_schema():
    """
    Тест для перевірки доступності OpenAPI схеми.
    """
    response = client.get("/openapi.json")
    assert response.status_code == 200, "OpenAPI schema is not accessible"
    assert (
        response.headers["content-type"] == "application/json"
    ), "Response is not JSON"
    assert "openapi" in response.json(), "OpenAPI schema is missing"

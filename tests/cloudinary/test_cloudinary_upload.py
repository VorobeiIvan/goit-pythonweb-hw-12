import pytest
import cloudinary.uploader
from cloudinary.exceptions import Error


@pytest.fixture
def test_image_path():
    """
    Фікстура для отримання шляху до тестового зображення.
    """
    return "tests/cloudinary/test_image.jpg"  # Замініть на реальний шлях до тестового зображення


def test_cloudinary_upload(test_image_path):
    """
    Тест для перевірки завантаження зображення у Cloudinary.
    """
    try:
        response = cloudinary.uploader.upload(test_image_path)
        assert "url" in response, "Response does not contain URL"
        assert response["secure_url"].startswith("https://"), "Secure URL is invalid"
    except Error as e:
        pytest.fail(f"Cloudinary upload failed: {e}")


def test_cloudinary_delete():
    """
    Тест для перевірки видалення зображення з Cloudinary.
    """
    # Завантажуємо тестове зображення
    upload_response = cloudinary.uploader.upload("tests/cloudinary/test_image.jpg")
    public_id = upload_response["public_id"]

    # Видаляємо зображення
    try:
        delete_response = cloudinary.uploader.destroy(public_id)
        assert delete_response["result"] == "ok", "Image was not deleted successfully"
    except Error as e:
        pytest.fail(f"Cloudinary delete failed: {e}")

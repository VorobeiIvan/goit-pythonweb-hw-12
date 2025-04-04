import subprocess
import os
import pytest


@pytest.fixture
def dockerfile_path():
    """
    Фікстура для отримання шляху до Dockerfile.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Dockerfile"))


@pytest.fixture
def image_name():
    """
    Фікстура для імені Docker-образу.
    """
    return "test_app_image"


def test_docker_build(dockerfile_path, image_name):
    """
    Тест для перевірки збірки Docker-образу.
    """
    assert os.path.exists(dockerfile_path), "Dockerfile does not exist"

    # Виконуємо команду для збірки Docker-образу
    result = subprocess.run(
        ["docker", "build", "-t", image_name, "-f", dockerfile_path, "."],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert result.returncode == 0, f"Docker build failed: {result.stderr}"


def test_docker_run(image_name):
    """
    Тест для перевірки запуску Docker-контейнера.
    """
    # Запускаємо контейнер
    result = subprocess.run(
        ["docker", "run", "--rm", image_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert result.returncode == 0, f"Docker container failed to run: {result.stderr}"

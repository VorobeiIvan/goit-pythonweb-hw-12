import subprocess
import os
import pytest


@pytest.fixture
def docker_compose_path():
    """
    Фікстура для отримання шляху до файлу docker-compose.yml.
    """
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../docker-compose.yml")
    )


def test_docker_compose_up(docker_compose_path):
    """
    Тест для перевірки запуску сервісів через Docker Compose.
    """
    assert os.path.exists(docker_compose_path), "docker-compose.yml does not exist"

    # Запускаємо сервіси через Docker Compose
    result = subprocess.run(
        ["docker-compose", "-f", docker_compose_path, "up", "-d"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert result.returncode == 0, f"Docker Compose up failed: {result.stderr}"

    # Зупиняємо сервіси після тесту
    subprocess.run(
        ["docker-compose", "-f", docker_compose_path, "down"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_docker_compose_services_running(docker_compose_path):
    """
    Тест для перевірки, чи сервіси працюють після запуску через Docker Compose.
    """
    # Запускаємо сервіси через Docker Compose
    subprocess.run(
        ["docker-compose", "-f", docker_compose_path, "up", "-d"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Перевіряємо статус сервісів
    result = subprocess.run(
        ["docker-compose", "-f", docker_compose_path, "ps"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert result.returncode == 0, f"Docker Compose ps failed: {result.stderr}"
    assert "Up" in result.stdout, "Some services are not running"

    # Зупиняємо сервіси після тесту
    subprocess.run(
        ["docker-compose", "-f", docker_compose_path, "down"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

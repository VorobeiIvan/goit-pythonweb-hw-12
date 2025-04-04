import os
import subprocess
import pytest


@pytest.fixture
def docs_path():
    """
    Фікстура для отримання шляху до папки з документацією.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docs"))


def test_sphinx_build(docs_path):
    """
    Тест для перевірки генерації документації Sphinx.
    """
    build_path = os.path.join(docs_path, "_build")
    try:
        # Виконуємо команду для побудови документації
        result = subprocess.run(
            ["sphinx-build", "-b", "html", docs_path, build_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        assert result.returncode == 0, f"Sphinx build failed: {result.stderr}"
    finally:
        # Очищення після тесту
        if os.path.exists(build_path):
            subprocess.run(["rm", "-rf", build_path])


def test_sphinx_index_html(docs_path):
    """
    Тест для перевірки наявності згенерованого файлу index.html.
    """
    build_path = os.path.join(docs_path, "_build", "index.html")
    try:
        # Генеруємо документацію
        subprocess.run(
            [
                "sphinx-build",
                "-b",
                "html",
                docs_path,
                os.path.join(docs_path, "_build"),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # Перевіряємо, чи існує index.html
        assert os.path.exists(build_path), "index.html was not generated"
    finally:
        # Очищення після тесту
        if os.path.exists(os.path.join(docs_path, "_build")):
            subprocess.run(["rm", "-rf", os.path.join(docs_path, "_build")])

import os
import sys

# Додати шлях до кореневої директорії проекту
sys.path.insert(0, os.path.abspath("../../"))

# Основні налаштування
project = "FastAPI Contacts Management API"
copyright = "2025, Ivan Vorobei"
author = "Ivan Vorobei"

# Розширення Sphinx
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinxcontrib.httpdomain",
]

# Тема для HTML
html_theme = "sphinx_rtd_theme"

# Шаблони та виключення
templates_path = ["_templates"]
exclude_patterns = []

# Увімкнення TODO
todo_include_todos = True

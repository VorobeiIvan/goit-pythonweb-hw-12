import os
import sys

# Add the path to the root directory of the project
sys.path.insert(0, os.path.abspath("../../"))

# Project metadata
project = "FastAPI Contacts Management API"  # The name of the project
copyright = "2025, Ivan Vorobei"  # Copyright information
author = "Ivan Vorobei"  # Author of the project

# Sphinx extensions to be used
extensions = [
    "sphinx.ext.autodoc",  # Automatically generate documentation from docstrings
    "sphinx.ext.napoleon",  # Support for Google and NumPy style docstrings
    "sphinx.ext.viewcode",  # Add links to highlighted source code
    "sphinx.ext.todo",  # Support for TODO directives in documentation
    "sphinxcontrib.httpdomain",  # Add support for documenting HTTP APIs
]

# HTML theme for the documentation
html_theme = "sphinx_rtd_theme"  # Use the Read the Docs theme for HTML output

# Paths for templates and files to exclude
templates_path = ["_templates"]  # Path to custom templates
exclude_patterns = []  # Patterns to exclude from the documentation build

# Enable TODO directives in the output
todo_include_todos = True  # Include TODO items in the generated documentation

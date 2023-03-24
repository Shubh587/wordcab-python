"""Sphinx configuration."""

import toml


with open("../pyproject.toml") as f:
    pyproject = toml.load(f)

project = "Wordcab Python"
author = "Wordcab"
copyright = "2022-2023, The Wordcab Team"

version = pyproject["tool"]["poetry"]["version"]
release = version

html_title = f"{project} v{version}"
html_last_updated_fmt = "%Y-%m-%d"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "sphinx_copybutton",
    "myst_parser",
]

autodoc_typehints = "description"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"

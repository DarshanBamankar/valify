import os
import sys

# Telling sphinx where our package source code lives
# so it can automatically read docstrings

sys.path.insert(0,os.path.abspath("../../src"))

# -------- Project Information --------------------------------------------------------------

project = "valify"
copyright = "2026, Darshan Bamankar"
author = "Darshan Bamankar"
release = "0.5.0"

# -------- General Configuration ------------------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",     # Reads docstrings automatically
    "sphinx.ext.viewcode",    # Adds "view source" links
    "sphinx.ext.napoleon",    # supports NumPy/Google style docstrings
]

templates_path = ["_templates"]
exclude_patterns = []

# -------- Options for HTML output ---------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

 


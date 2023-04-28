# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'COOLEST'
copyright = '2023, COOLEST developers'
author = 'COOLEST developers'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',  # prints compilation durations
    'sphinx.ext.autodoc',  # documentation based on docstrings
    'sphinx.ext.autosummary',  # generates class descriptions based on code
    'sphinx.ext.napoleon' # generates .rst pages based on package modules
    'sphinx.ext.viewcode',  # adds links to highlighted code
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'  # third-party theme
html_static_path = ['_static']

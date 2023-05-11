# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


from datetime import date
import coolest


project = 'COOLEST'
copyright = f"{date.today().year}, COOLEST developers "
author = coolest.__author__
release = coolest.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',  # prints compilation durations
    'sphinx.ext.autodoc',  # documentation based on docstrings
    'sphinx.ext.autosummary',  # generates class descriptions based on code
    'sphinx.ext.napoleon', # generates .rst pages based on package modules
    'sphinx.ext.viewcode',  # adds links to highlighted code
    'myst_nb',  # supports markdown .md files
    'sphinx_design', # responsive design components
    'autoapi.extension',  # generates autoapi directory
    "sphinx_math_dollar",  # allows to write LaTeX in .md files
    "sphinxcontrib.bibtex",
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# AutoAPI configuration
autoapi_dirs = ["../coolest"]
autoapi_type = "python"
autoapi_add_toctree_entry = False
autoapi_options = ["show-module-summary", "undoc-members"]
autodoc_typehints = "signature"
# autoapi_python_class_content = 'both'  # includes both class and __init__ docstrings

# Options for HTML output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'  # third-party theme
html_static_path = ['_static']

# Suffixes to support with myst_parser
source_suffix = {
    ".rst": "restructuredtext", 
    ".ipynb": "myst-nb", 
    ".md": "myst-nb"
}

nb_custom_formats = {
    ".md": ["jupytext.reads", {"fmt": "mystnb"}],
}
myst_enable_extensions = ["colon_fence"]

autosummary_generate = True
add_module_names = False  # prevent cluttering the doc with the full submodule path

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_title = ""
html_logo = "_static/coolest_logo.png"
html_css_files = ["custom.css"]

# Skip files we do not want to be included in the documentation
def skip_util_classes(app, what, name, obj, skip, options):
    excluded_modules = [
        "coolest.template.info",
        "coolest.template.lazy",
        "coolest.template.classes.regularization",
        "coolest.template.classes.regularization_list",
    ]
    if what == "module" and name in excluded_modules:
        skip = True

    excluded_packages = [
        "coolest.template.classes.regularization",
        "coolest.template.classes._old",
    ]
    if what == "package" and name in excluded_packages:
        skip = True

    return skip

def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_util_classes)


bibtex_bibfiles = ["refs.bib"]
bibtex_default_style = "alpha"  # alpha, plain, unsrt, unsrtalpha

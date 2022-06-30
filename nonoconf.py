# Configuration file for the Sphinx documentation builder.

# -- Project information

project = "ical-reader"
copyright = "2022, Jorrick Sleijster"
author = "Jorrick Sleijster"

release = "0.1.0"
version = "0.1.0a1"

# -- General configuration

extensions = [
    # "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    # "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.duration",
    "sphinx.ext.linkcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
]
extensions.append("autoapi.extension")

autoapi_type = "python"
autoapi_dirs = ["../src/ical_reader"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"

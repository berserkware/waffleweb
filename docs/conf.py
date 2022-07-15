
# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Waffleweb'
copyright = '2022, Caleb Mckay'
author = 'Caleb Mckay'

version = '0.1a2'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
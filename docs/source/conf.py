import sys
import os

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))

project = "company-orders"
copyright = "2024, David Landa"
author = "David Landa"

# ########################################################################## #

extensions = [
    "nbsphinx",
    "myst_parser",
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    "sphinxcontrib.scm",
    "sphinx_github_changelog",
]

# ########################################################################## #
templates_path = ["_templates"]
exclude_patterns = []

# ########################################################################## #

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# ########################################################################## #
scm_contribs_email = "true"
scm_contribs_limit_contributors = None  
scm_contribs_min_commits = 1            
scm_contribs_sort = "num"
scm_contribs_type ="committer"          

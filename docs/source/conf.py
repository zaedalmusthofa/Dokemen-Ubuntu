# Configuration file for the Sphinx documentation builder.

# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath('../../src'))

# -- Project information -----------------------------------------------------

project = 'MoilApp Documentation'
copyright = '2024, Perseverance Technology, Taiwan'
author = 'Haryanto'

# The full version, including alpha/beta/rc tags
release = '4.1'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc",
              "sphinx.ext.viewcode",
              "sphinx.ext.napoleon",
              ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []
html_logo = "assets/light-moilapp.png"
html_theme_options = {'logo_only': True, 'display_version': False, }

master_doc = 'index'

autoclass_content = 'both'
autodoc_mock_imports = ["moilutils", "Moildev", "PyQt6", "cv2",
                        "numpy", "models.main_model", "pyexiv2",
                        "git"]
html_show_sourcelink = False

autodoc_default_flags = ['members']
autodoc_member_order = 'bysource'
autodoc_default_options = {'undoc-members': True, }

latex_elements = {'extraclassoptions': 'openany,oneside'}
latex_font_size = '12pt,oneside'

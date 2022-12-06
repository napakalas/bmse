# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'BMSE: Biosimulation Model Search Engine'
copyright = '2022, Yuda Munarko'
author = 'Yuda Munarko'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme',
    'sphinxarg.ext',
    'sphinxcontrib.bibtex',
]
myst_enable_extensions = ["colon_fence"]

# templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

bibtex_bibfiles = ['refs.bib']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']

# -- Options for Latex output ------------------------------------------------

latex_elements = {
    'papersize': 'a4paper',
    }

latex_docclass = {
   'howto': 'article',
   'manual': 'report',
}

# # -- Ensure apidoc is run ----------------------------------------------------
# 
# def run_apidoc(app, config):
#     """
#     Hook to generate API documentation via sphinx-apidoc
#     Args:
#         app : the Sphinx application
#         config : the Sphinx configuration
#     """
#     import sphinx.ext.apidoc
# 
#     args = [
#         "--force",
#         "--separate",
#         "--output-dir", "_source",
#         "../mapmaker"
#     ]
#     sphinx.ext.apidoc.main(args)
# 
# def setup(app):
#     app.connect("config-inited", run_apidoc)
# 
# # -- End of File -------------------------------------------------------------
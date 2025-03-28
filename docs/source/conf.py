import os
import sys


sys.path.insert(0, os.path.abspath("../../"))
# sys.path.insert(0, os.path.abspath("../../model"))
# sys.path.insert(0, os.path.abspath("../../oic_model_server"))
# sys.path.insert(0, os.path.abspath("../../streamlit_app"))

project = 'mini-proyecto-oic'
copyright = '2025, Luis Andres Campos Maldonado'
author = 'Luis Andres Campos Maldonado'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]


templates_path = ["_templates"]
html_theme = "sphinx_rtd_theme"
html_logo = "./_static/logo_python.jpg"
html_static_path = ["_static"]

html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": True,
    "sticky_navigation": True,
    "titles_only": False,
    "logo_only": False,
}

autodoc_default_options = {
    'no-signature': True,
}

# html_context = {
#     "style": "default"
# }

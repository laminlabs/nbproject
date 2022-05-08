from datetime import datetime
import nbproject  # noqa
import sys
from pathlib import Path
from sphinx.application import Sphinx

HERE = Path(__file__).parent
sys.path[:0] = [str(HERE.parent), str(HERE / "extensions")]
import nbproject  # noqa

for generated in HERE.glob("nbproject.*.rst"):
    generated.unlink()

project = "nbproject"
author = "Lamin Labs"
copyright = f"{datetime.now():%Y}, {author}"
release = nbproject.__version__.replace(".dirty", "")

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "IPython.sphinxext.ipython_console_highlighting",  # noqa https://github.com/spatialaudio/nbsphinx/issues/24
    "myst_nb",
    *[p.stem for p in (HERE / "extensions").glob("*.py")],
]

templates_path = ["lamin-sphinx-theme/_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**.ipynb_checkpoints",
    "README.md",
    ".pytest_cache/*",
]

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "show_prev_next": False,
    "use_edit_page_button": False,  # currently unused
    "search_bar_text": "Search",  # currently unused
    "navbar_end": ["theme-switcher"],
    "navbar_align": "left",
    "footer_items": ["copyright"],
}

html_context = {
    "default_mode": "auto",
    "github_user": "laminlabs",
    "github_repo": "nbproject",
    "github_version": "main",
}

html_title = "nbproject | Lamin Labs"
html_logo = "lamin-sphinx-theme/_static/img/logo.svg"
html_favicon = "lamin-sphinx-theme/_static/img/favicon.ico"
html_static_path = ["lamin-sphinx-theme/_static"]

html_sidebars = {
    "**": ["sidebar-nav-bs"],
}

source_suffix = [".md", ".ipynb"]
master_doc = "index"
default_role = "literal"

# Generate the API documentation
autosummary_generate = True
autodoc_member_order = "bysource"
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_use_rtype = True  # having a separate entry generally helps readability
napoleon_use_param = True
todo_include_todos = False
nitpicky = True  # report broken links


def setup(app: Sphinx):
    # Don’t allow broken links. DO NOT CHANGE THIS LINE, fix problems instead.
    app.warningiserror = False
    app.add_css_file("custom.css")

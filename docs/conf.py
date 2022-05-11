import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path[:0] = [str(HERE)]
from lamin_sphinx import *  # noqa
import nbproject  # noqa

project = "nbproject"
html_title = f"{project} | Lamin Labs"
release = nbproject.__version__
html_context["github_repo"] = "nbproject"  # noqa

ogp_site_url = "https://lamin.ai/nbproject"

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path[:0] = [str(HERE)]
from lamin_sphinx import *  # noqa
import nbproject  # noqa

for generated in HERE.glob("nbproject.*.rst"):
    generated.unlink()

project = "nbproject"
html_title = f"{nbproject} | Lamin Labs"
release = nbproject.__version__
html_context["github_repo"] = "nbproject"  # noqa
html_sidebars = {
    "*": [],
}

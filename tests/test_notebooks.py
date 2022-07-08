from pathlib import Path

from nbproject._logger import logger
from nbproject.dev import test


def test_notebooks():
    # assuming this is in the tests folder
    docs_folder = Path(__file__).parents[1] / "docs/"

    for check_folder in docs_folder.glob("./**"):
        # the following are the typical notebook test paths
        # if not str(check_folder).endswith(("guides", "tutorials")):
        #     continue
        # usually we specify them in pyproject.toml via
        # [tool.pytest.ini_options]
        # testpaths = [
        #     "tests",
        #     "docs/tutorials",
        #     "docs/guides",
        # ]
        # here, we need to specify them manually
        logger.debug(f"\n{check_folder}")
        test.execute_notebooks(check_folder, write=True)

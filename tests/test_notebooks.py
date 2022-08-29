from pathlib import Path

from nbproject._logger import logger
from nbproject.dev import test


def test_notebooks():
    docs_folder = Path(__file__).parents[1] / "docs/"

    for check_folder in docs_folder.glob("./**"):
        logger.debug(f"\n{check_folder}")
        test.execute_notebooks(check_folder, write=True)

from pathlib import Path

from nbproject.dev import test


def test_notebooks():
    # assuming this is in the tests folder
    nb_folder = Path(__file__).parents[1] / "docs/guides"

    test.execute_notebooks(nb_folder, write=True)

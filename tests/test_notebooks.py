import os
from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

from nbproject._logger import logger


def execute_notebooks(nb_folder: Path, write: bool = True):

    notebooks = nb_folder.glob("**/*.ipynb")

    for nb in notebooks:
        nb_name = str(nb.relative_to(nb_folder))
        logger.debug(f"\n{nb_name}")

        nb_content = nbf.read(nb, as_version=nbf.NO_CONVERT)

        client = NotebookClient(nb_content)

        os.environ["NBPRJ_TEST_NBPATH"] = str(nb)

        client.execute(env=os.environ)

        if write:
            nbf.write(nb_content, nb)


def test_notebooks():
    # assuming this is in the tests folder
    nb_folder = Path(__file__).parents[1] / "docs/guides"

    execute_notebooks(nb_folder, write=True)

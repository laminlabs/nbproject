import os
from pathlib import Path

from .._logger import logger


def execute_notebooks(nb_folder: Path, write: bool = True):
    """Execute all notebooks in the folder.

    Args:
        nb_folder: Path to folder with the notebooks to execute.
        write: If `True`, write the execution results to the notebooks.
    """
    from nbclient import NotebookClient
    from nbformat import NO_CONVERT
    from nbformat import read as read_nb
    from nbformat import write as write_nb

    env = dict(os.environ)

    os.chdir(nb_folder)

    notebooks = nb_folder.glob("**/*.ipynb")

    for nb in notebooks:
        nb_name = str(nb.relative_to(nb_folder))
        logger.debug(f"\n{nb_name}")

        nb_content = read_nb(nb, as_version=NO_CONVERT)

        client = NotebookClient(nb_content)

        env["NBPRJ_TEST_NBPATH"] = str(nb)

        client.execute(env=env)

        if write:
            write_nb(nb_content, nb)

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

    # notebooks are part of documentation and indexed
    # by a sphinx myst index.md file
    # the order of execution matters!
    notebooks = []

    index_path = nb_folder / "index.md"
    if index_path.exists():
        with open(index_path) as f:
            index = f.read()

        # parse out indexed file list
        if "```{toctree}" in index:
            content = index.split("```{toctree}")[1]
            content = content.split("\n\n")[1]
            content = content.split("```")[0]

            # if a file is a notebook, add it
            for name in content.split():
                nb = nb_folder / f"{name}.ipynb"
                if nb.exists():
                    notebooks.append(nb)

    for nb in nb_folder.glob("./*.ipynb"):
        if nb not in notebooks:
            notebooks.append(nb)

    for nb in notebooks:
        if ".ipynb_checkpoints/" in str(nb):
            continue
        nb_name = str(nb.relative_to(nb_folder))
        logger.debug(f"{nb_name}")

        nb_content = read_nb(nb, as_version=NO_CONVERT)

        client = NotebookClient(nb_content)

        env["NBPRJ_TEST_NBPATH"] = str(nb)

        client.execute(env=env)

        if write:
            write_nb(nb_content, nb)

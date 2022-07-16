from typing import Optional

from ._logger import logger
from ._meta import _load_meta
from .dev._consecutiveness import check_consecutiveness
from .dev._jupyter_lab_commands import _save_notebook
from .dev._notebook import Notebook, read_notebook


def _check_last_cell(nb: Notebook, code: str) -> bool:
    last_code_cell = None
    for cell in nb.cells:
        if cell["cell_type"] == "code" and cell["source"] != []:
            last_code_cell = cell

    if last_code_cell is not None and code in "".join(last_code_cell["source"]):
        return True
    else:
        return False


def publish(
    *,
    version: Optional[str] = None,
    dependency: bool = True,
    consecutiveness: bool = True,
    i_confirm_i_saved: bool = False,
    last_cell: bool = True,
    **kwargs,
):
    """Publish your notebook before sharing it to ensure it's reproducible.

    This function should be called in the last code cell of the notebook!

    1. Checks that the notebook has a title.
    2. Sets the version.
    3. Stores dependencies.
    4. Checks consecutiveness, i.e., whether notebook cells were executed consecutively.

    Returns the consecutiveness check result.

    Args:
        version: If `None`, bumps the version from "draft" to "1", from "1" to "2", etc.
            Otherwise sets the version to the passed version.
        dependency: If `True`, writes `dependency.live` to `dependency.store`.
            If `False`, leaves the current `dependency.store` as is.
        consecutiveness: If `False`, does not check consecutiveness.
        i_confirm_i_saved: Only relevant outside Jupyter Lab as a safeguard against
            losing the editor buffer content because of accidentally publishing.
        last_cell: If `True`, checks that `publish` is in the last code cell
            of the notebook.
    """
    meta = _load_meta()
    if "calling_statement" in kwargs:
        calling_statement = kwargs["calling_statement"]
    else:
        calling_statement = "publish("

    notebook_title = meta.live.title
    title_error = (
        "Error: No title! Please update & save your notebook so that it has a"
        " markdown cell with the title: # My title"
    )

    if notebook_title is None:
        raise RuntimeError(title_error)

    if meta._env == "lab":
        _save_notebook()
    else:
        if not i_confirm_i_saved:
            raise RuntimeError(
                "Make sure you save the notebook in your editor before publishing!\n"
                "You can avoid the need for manually saving in Jupyter Lab, which auto-saves the buffer during publish."  # noqa
            )

    nb = read_notebook(meta._filepath)

    if last_cell and not _check_last_cell(nb, calling_statement):
        raise RuntimeError("publish is not at the end of the current notebook.")

    if consecutiveness:
        check_consecutiveness(nb, ignore_code=calling_statement)

    if version is not None:
        meta.store.version = version
    else:
        try:
            if meta.store.version == "draft":
                version = "1"
            else:
                version = str(int(meta.store.version) + 1)  # bump version by 1
            meta.store.version = version
        except ValueError:
            raise ValueError(
                "The nbproject version cannot be cast to integer. Please pass a version"
                " string."
            )

    info = f"Bumped notebook version to {version}."

    if dependency:
        meta.store.dependency = meta.live.dependency
        info += " Wrote dependencies to dependency store."

    logger.info(info)

    meta.store.write()

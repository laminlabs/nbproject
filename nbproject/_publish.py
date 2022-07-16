from typing import Optional

from ._logger import logger
from ._meta import _load_meta
from .dev._check_last_cell import check_last_cell
from .dev._consecutiveness import check_consecutiveness
from .dev._jupyter_lab_commands import _save_notebook
from .dev._notebook import read_notebook


def publish(
    *,
    version: Optional[str] = None,
    i_confirm_i_saved: bool = False,
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
        i_confirm_i_saved: Only relevant outside Jupyter Lab as a safeguard against
            losing the editor buffer content because of accidentally publishing.
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
        pretend_no_test_env = (
            kwargs["pretend_no_test_env"] if "pretend_no_test_env" in kwargs else False
        )
        if (
            meta._env == "test" and not pretend_no_test_env
        ):  # do not raise error in test environment
            pass
        elif not i_confirm_i_saved:
            raise RuntimeError(
                "Make sure you save the notebook in your editor before publishing!\n"
                "You can avoid the need for manually saving in Jupyter Lab, which auto-saves the buffer during publish."  # noqa
            )

    nb = read_notebook(meta._filepath)
    if not check_last_cell(nb, calling_statement):
        raise RuntimeError("Can only publish from the last code cell of the notebook.")
    check_consecutiveness(nb)

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

    meta.store.dependency = meta.live.dependency
    logger.info(f"Bumped notebook version to {version} & wrote dependencies.")

    meta.store.write()

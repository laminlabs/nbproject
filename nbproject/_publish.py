from typing import Optional

from ._logger import logger
from ._meta import _load_meta
from .dev._integrity import check_integrity
from .dev._jupyter_lab_commands import _save_notebook
from .dev._notebook import read_notebook


def publish(
    version: Optional[str] = None,
    dependency: bool = True,
    integrity: bool = True,
    i_confirm_i_saved: bool = False,
):
    """Publish your notebook before sharing it to ensure it's reproducible.

    1. Sets the version.
    2. Stores dependencies.
    3. Checks integrity, i.e., whether notebook cells were executed consecutively.

    Returns the integrity check result.

    Args:
        version: If `None`, bumps the version from "draft" to "1", from "1" to "2", etc.
            Otherwise sets the version to the passed version.
        dependency: If `True`, writes `dependency.live` to `dependency.store`.
            If `False`, leaves the current `dependency.store` as is.
        integrity: If `False`, does not check integrity.
        i_confirm_i_saved: Only relevant outside Jupyter Lab as a save guard against
            losing the editor buffer content because of accidentally publishing.
    """
    meta = _load_meta()

    if meta._env == "lab":
        _save_notebook()
    else:
        if not i_confirm_i_saved:
            raise RuntimeError(
                "Make sure you save the notebook in your editor before publishing!\n"
                "You can avoid the need for manually saving in Jupyter Lab, which auto-saves the buffer during publish."  # noqa
            )

    if integrity:
        check_integrity(read_notebook(meta._filepath), ignore_code="publish(")

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

    meta.store.write(restart=False)

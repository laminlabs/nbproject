from typing import Optional

from ._logger import logger
from ._meta import _load_meta
from .dev._integrity import check_integrity
from .dev._jupyter_lab_commands import _save_notebook
from .dev._notebook import read_notebook


def publish(
    version: Optional[str] = None,
    store_dependency: bool = True,
    integrity: bool = True,
):
    """Publish the notebook.

    1. Sets the version.
    2. Stores dependencies.
    3. Checks integrity, i.e., whether notebook cells were executed consecutively.

    Returns the integrity check result.

    Args:
        version: If `None`, bumps the version from "draft" to "1", from "1" to "2", etc.
            Otherwise sets the version to the passed version.
        store_dependency: If `True`, writes `dependency.live` to `dependency.store`.
            If `False`, leaves the current `dependency.store` as is.
        integrity: If `False`, does not check integrity.
    """
    meta = _load_meta()

    if meta._env == "lab":
        _save_notebook()
    elif meta._env != "test":
        logger.warning(
            "If not on Jupyter Lab, save the notebook before publishing!\n"
            "The file changes on disk during publishing and the buffer is overwritten."
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

    if store_dependency:
        meta.store.dependency = meta.live.dependency
        info += " Wrote dependencies to dependency store."

    logger.info(info)

    meta.store.write(restart=False)

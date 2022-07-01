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
    else:
        logger.info("Save the notebook before publishing.")

    check = None
    if integrity:
        check = check_integrity(read_notebook(meta._filepath), ignore_code="publish(")

    if version is not None:
        meta.store.version = version
    else:
        try:
            if meta.store.version == "draft":
                version = "1"
            else:
                # bump version by 1
                version = str(int(meta.store.version) + 1)
            meta.store.version = version
        except ValueError:
            raise ValueError(
                "The nbproject version is not an integer, please specify a version"
                " string to set."
            )

    logger.info(f"... set notebook version to {version}")

    if store_dependency:
        meta.store.dependency = meta.live.dependency
        logger.info("... wrote dependencies to dependency store")

    meta.write(restart=False)

    return check

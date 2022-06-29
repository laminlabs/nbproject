from typing import Optional

from ._logger import logger
from ._meta import _load_meta
from .dev._integrity import check_integrity
from .dev._jupyter_lab_commands import _save_notebook
from .dev._notebook import read_notebook


def publish(
    version: Optional[str] = None,
    store_dependency: bool = True,
    ignore_integrity: bool = False,
):
    """Publish the notebook.

    1. Sets version.
    2. Tracks dependencies.
    3. Runs `check_integrity`.

    Returns a report about the integrity of the notebook.

    Args:
        version: If `None`, bumps the version from "draft" to 1, from 1 to 2, etc.
            Otherwise sets the version to the passed version.
        store_dependency: If `True`, writes `dependency.live` to `dependency.store`.
            If `False`, leaves the current `dependency.store` as is.
        ignore_integrity: If `True`, does not check integrity before publishing.
    """
    meta = _load_meta()

    if meta._env == "lab":
        _save_notebook()
    else:
        logger.info("Save the notebook before publishing.")

    if ignore_integrity:
        integrity = True
    else:
        integrity = check_integrity(
            read_notebook(meta._filepath), ignore_code="publish("
        )

    if not integrity:
        raise ValueError("The notebook cells were not run consequently.")

    if version is not None:
        meta.store.version = version
    else:
        try:
            if meta.store.version != "draft":
                version = str(int(meta.store.version) + 1)
            else:
                version = "1"
            meta.store.version = version
        except ValueError:
            raise ValueError(
                "The nbproject version is not an integer, please specify a version"
                " string to set."
            )

    if store_dependency:
        meta.store.dependency = meta.live.dependency

    logger.info("Your notebook seems great & reproducible! I love it.")

    meta.write()

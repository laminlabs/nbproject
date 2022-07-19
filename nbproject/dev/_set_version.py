from typing import Union

from .._logger import logger
from .._meta import meta


def set_version(
    version: Union[str, None] = None, stored_version: Union[str, None] = None
):
    """(Auto-) set version.

    If `None`, bumps the version from "draft" to "1", from "1" to "2", etc.
    Otherwise sets the version to the passed version.

    Args:
        version: Pass version string.
        stored_version: Mock stored version for testing purposes.
    """
    if stored_version is None:
        stored_version = meta.store.version

    if version is not None:
        return version
    else:
        try:
            if stored_version == "draft":
                version = "1"
            else:
                version = str(int(stored_version) + 1)  # increment version by 1
            return version
        except ValueError:
            logger.error("The version cannot be auto-set. Please pass a version.")
            return "manual-version"

from typing import Union

from nbproject._meta import meta


def set_version(
    version: Union[str, None] = None, stored_version: Union[str, None] = None
):
    """(Auto-) set version.

    If `version` is `None`, returns the stored version.
    Otherwise sets the version to the passed version.

    Args:
        version: Version string.
        stored_version: Mock stored version for testing purposes.
    """
    if stored_version is None:
        stored_version = meta.store.version

    if version is not None:
        return version
    else:
        return stored_version

"""nbproject: Manage your notebooks."""

__version__ = "0.1.0dev"

from ._header import Header  # noqa

from . import _version

__version__ = _version.get_versions()["version"]

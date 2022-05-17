"""nbproject: Manage your notebooks."""
import traceback
import sys
from types import ModuleType

from ._header import Header  # noqa


class LazyVersion(ModuleType):
    @property
    def __version__(self):
        from ._version import get_versions

        return get_versions()["version"]


sys.modules[__name__].__class__ = LazyVersion


def within_flit():
    for frame in traceback.extract_stack():
        if frame.name == "get_docstring_and_version_via_import":
            return True
    return False


if within_flit():
    sys.modules[__name__].__dict__["__version__"] = sys.modules[__name__].__version__

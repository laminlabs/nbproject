"""nbproject: Manage your notebooks."""
import sys
from types import ModuleType

from ._header import Header  # noqa


class LazyVersion(ModuleType):
    @property
    def __version__(self):
        from ._version import get_versions

        return get_versions()["version"]


sys.modules[__name__].__class__ = LazyVersion

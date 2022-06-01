"""nbproject: Manage Jupyter notebooks.

Display `nbproject` metadata with default arguments::

   from nbproject import header

Display with configurable arguments & update::

   from nbproject import Header
   header = Header(*args, **kwargs)
   header.infer_dependencies()

The API consists of a class `Header`.
The "module" `header` offers a mere shortcut for initializing it with default arguments.

.. autosummary::
   :toctree: .

   Header
"""
import traceback
import sys
from types import ModuleType

from ._header import Header  # noqa

_module = sys.modules[__name__]


class LazyVersion(ModuleType):
    @property
    def __version__(self):
        from ._version import get_versions

        return get_versions()["version"]


_module.__class__ = LazyVersion


def within_flit():
    for frame in traceback.extract_stack():
        if frame.name == "get_docstring_and_version_via_import":
            return True
    return False


if within_flit():
    _module.__dict__["__version__"] = _module.__version__

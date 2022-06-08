"""nbproject: Manage Jupyter notebooks.

Display `nbproject` metadata with default arguments::

   from nbproject import header

Access `nbproject` metadata through the API::

   from nbproject import meta

Display with configurable arguments & update::

   from nbproject import Header
   header = Header(*args, **kwargs)
   header.infer_dependencies()

The API consists of a single class `Header`.

.. autosummary::
   :toctree: .

   Header

The one-liner `from nbproject import header` offers a mere shortcut for
initializing `Header` with default arguments!
"""
import sys
import traceback
from types import ModuleType

from ._header import Header  # noqa
from ._meta import _load_meta  # noqa


# see this for context: https://stackoverflow.com/questions/880530
def __getattr__(name):  # user experience is that of a property on a class!
    if name == "meta":  # there is a bit of weird behavior because it seems
        return _load_meta()  # to be called twice only upon from nbproject import meta
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


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

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
__version__ = "0.0.9"

import sys
from types import ModuleType

from ._header import Header  # noqa

_module = sys.modules[__name__]


class LazyMeta(ModuleType):
    @property
    def meta(self):
        from ._meta import _load_meta

        return _load_meta()


_module.__class__ = LazyMeta

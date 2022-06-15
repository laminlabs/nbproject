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
    _meta = None

    @property
    def meta(self):
        if self._meta is None:
            from ._meta import _load_meta

            self._meta = _load_meta()

        return _meta


_module.__class__ = LazyMeta

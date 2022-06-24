"""nbproject: Manage Jupyter notebooks.

.. currentmodule:: nbproject

Display `nbproject` metadata with default arguments::

   from nbproject import header

Get fine-grained access to `nbproject` via::

   from nbproject import meta

The static class `meta` allows access to live and an on-disk metadata store via:

   meta.store
   meta.live

These return instances of the corresponding classes:

.. autoclass:: MetaStore
   :members:
   :undoc-members:

.. autoclass:: MetaLive
   :members:
   :undoc-members:

Similarly, `header` is an instance of `Header` and `meta` an instance of `Meta`:

.. autosummary::
   :toctree:

   Header
   Meta

For even more fine-grained access, we offer a developer API:

.. autosummary::
   :toctree: .

   dev

"""
__version__ = "0.1a3"

from . import dev
from ._header import Header  # noqa
from ._meta import Meta, MetaLive, MetaStore

_meta = None
# see this for context: https://stackoverflow.com/questions/880530
def __getattr__(name):  # user experience is that of a property on a class!
    global _meta

    if name == "meta":
        if _meta is None:
            from ._meta import _load_meta

            _meta = _load_meta()
        return _meta

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

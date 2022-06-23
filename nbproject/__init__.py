"""nbproject: Manage Jupyter notebooks.

Display `nbproject` metadata with default arguments::

   from nbproject import header

Access `nbproject` metadata through the API::

   from nbproject import meta
   meta.store
   meta.live.dependency
   meta.live.title
   meta.live.integrity
   meta.live.time_run
   meta.live.time_passed

You can access developer functions via `nbproject.dev`.

Display with configurable arguments & update::

   from nbproject import Header
   header = Header(*args, **kwargs)

The one-liner `from nbproject import header` offers a mere shortcut for
initializing `Header` with default arguments.

.. autoclass:: Header
   :members:
   :undoc-members:

For more detailed control, we offer an instance of `Meta` via `nbproject.meta`.

.. autoclass:: Meta
   :members:
   :undoc-members:

The `nbproject.meta.live` gives access to live metadata of the current notebook
and is an instance of

.. autoclass:: MetaLive
   :members:
   :undoc-members:

The `nbproject.meta.store` stores nbproject metadata from the current notebook file
and is an instance of

.. autoclass:: MetaStore
   :members:
   :undoc-members:
"""
__version__ = "0.1a2"

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

    if name == "dev":
        from ._dev import init_dev

        return init_dev

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

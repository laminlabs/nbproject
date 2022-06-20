"""nbproject: Manage Jupyter notebooks.

Display `nbproject` metadata with default arguments::

   from nbproject import header

Access `nbproject` metadata through the API::

   from nbproject import meta
   meta.store
   meta.live.dependency
   meta.live.title

Display with configurable arguments & update::

   from nbproject import Header
   header = Header(*args, **kwargs)

The API consists of.

.. autosummary::
   :toctree: .

   meta

The one-liner `from nbproject import header` offers a mere shortcut for
initializing `Header` with default arguments!
"""
__version__ = "0.0.9"

from ._header import Header  # noqa
from ._meta import meta


# see this for context: https://stackoverflow.com/questions/880530
def __getattr__(name):  # user experience is that of a property on a class!

    if name == "meta":
        from ._meta import meta

        return meta

    if name == "dev":
        from ._dev import init_dev

        return init_dev

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

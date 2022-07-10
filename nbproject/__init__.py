"""nbproject: Manage Jupyter notebooks.

.. currentmodule:: nbproject

Display metadata with default arguments and start tracking with class instance `header`::

   from nbproject import header

.. autosummary::
   :toctree:

   header

Publish your notebook before sharing it with someone to ensure they can reproduce it.

.. autosummary::
   :toctree:

   publish

To access metadata use the class instance `meta`::

   from nbproject import meta

.. autosummary::
   :toctree:

   Meta

It offers access to `meta.store` and `meta.live`:

.. autosummary::
   :toctree:

   MetaContainer
   MetaStore
   MetaLive

For more fine-grained access, we offer a developer API:

.. autosummary::
   :toctree: .

   dev

"""
__version__ = "0.1.6"

from . import dev
from ._header import header  # noqa
from ._meta import Meta, MetaContainer, MetaLive, MetaStore
from ._publish import publish

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

"""nbproject: Manage Jupyter notebooks.

.. currentmodule:: nbproject

Most users will only need these two functions:

.. autosummary::
   :toctree:

   header
   publish

Use them with default arguments after importing them like this::

   from nbproject import header, publish

To access metadata use the class instance `meta`::

   from nbproject import meta

.. autosummary::
   :toctree:

   Meta
   MetaLive

For more fine-grained access, we offer a developer API:

.. autosummary::
   :toctree: .

   dev

"""
__version__ = "0.3.1"

from . import dev
from ._header import header  # noqa
from ._meta import Meta, MetaLive
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

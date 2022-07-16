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

   meta
   MetaLive

For more fine-grained access, we offer a developer API:

.. autosummary::
   :toctree: .

   dev

"""
__version__ = "0.3.1"

from . import dev
from ._header import header  # noqa
from ._meta import MetaLive, meta
from ._publish import publish

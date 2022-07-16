"""nbproject: Manage Jupyter notebooks.

.. currentmodule:: nbproject

Most users will only need these two functions:

.. autosummary::
   :toctree:

   header
   publish

Use them with default arguments after importing them like this::

   from nbproject import header, publish

For more fine-grained access, see:

.. autosummary::
   :toctree:

   meta
   dev

"""
__version__ = "0.3.1"

from . import dev
from ._header import header
from ._meta import meta
from ._publish import publish

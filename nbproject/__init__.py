"""nbproject: Manage Jupyter notebooks.

.. currentmodule:: nbproject

Most users will only need these two functions:

.. autosummary::
   :toctree:

   header
   publish

Use them with default arguments after importing them like this::

   from nbproject import header, publish

For more fine-grained access, use:

.. autosummary::
   :toctree:

   meta
   dev

"""
__version__ = "0.10.6"

from .dev._jupyter_lab_commands import _init_frontend

# init jupyter lab frontend immediately on import
# nothing happens if this is not jupyter lab
try:
    _init_frontend()
except:  # noqa: E722
    pass

from . import dev
from ._header import header
from ._meta import meta
from ._publish import publish

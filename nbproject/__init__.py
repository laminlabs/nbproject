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
__version__ = "0.8.1"

from .dev._classic_nb_commands import _set_nbclassic_path
from .dev._jupyter_lab_commands import _init_frontend

# init jupyter lab frontend immediately on import
# nothing happens if this is not jupyter lab
_init_frontend()
# tries to set the NBCLASSIC_PATH env variable for classical notebook or nbclassic
_set_nbclassic_path()

from . import dev
from ._header import header
from ._meta import meta
from ._publish import publish

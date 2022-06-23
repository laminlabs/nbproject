"""Developer functions.

.. autoclass:: Notebook
   :members:
   :undoc-members:

"""
from . import _test as test
from ._dependency import infer_dependencies
from ._initialize import initialize_metadata
from ._integrity import check_integrity
from ._jupyter_communicate import notebook_path
from ._notebook import read_notebook, write_notebook, Notebook

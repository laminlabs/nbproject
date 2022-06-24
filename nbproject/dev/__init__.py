"""Developer functions.

Features
--------

.. autofunction:: infer_dependencies
.. autofunction:: check_integrity

Backend
-------

.. autofunction:: initialize_metadata
.. autofunction:: notebook_path
.. autoclass:: Notebook
.. autofunction:: read_notebook
.. autofunction:: write_notebook
"""
from . import _test as test
from ._dependency import infer_dependencies
from ._initialize import initialize_metadata
from ._integrity import check_integrity
from ._jupyter_communicate import notebook_path
from ._notebook import Notebook, read_notebook, write_notebook

"""Developer API.

Features
--------

.. autofunction:: infer_dependencies_from_nb
.. autofunction:: infer_dependencies_from_file
.. autofunction:: check_consecutiveness

Backend
-------

.. autofunction:: initialize_metadata
.. autofunction:: notebook_path
.. autoclass:: Notebook
.. autofunction:: read_notebook
.. autofunction:: write_notebook
"""
import nbproject_test as test

from ._consecutiveness import check_consecutiveness
from ._dependency import infer_dependencies_from_file, infer_dependencies_from_nb
from ._initialize import initialize_metadata
from ._jupyter_communicate import notebook_path
from ._notebook import Notebook, read_notebook, write_notebook

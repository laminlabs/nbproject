"""Developer API.

Metadata
--------

.. autosummary::
   :toctree:

   MetaLive
   MetaStore
   MetaContainer

Functionality
-------------

.. autofunction:: infer_pypackages_from_nb
.. autofunction:: infer_pypackages_from_file
.. autofunction:: check_consecutiveness
.. autofunction:: set_version

Helpers
-------

.. autofunction:: initialize_metadata
.. autoclass:: Notebook
.. autofunction:: notebook_path
.. autofunction:: read_notebook
.. autofunction:: write_notebook
"""
import nbproject_test as test

from ._consecutiveness import check_consecutiveness
from ._initialize import initialize_metadata
from ._jupyter_communicate import notebook_path
from ._meta_live import MetaLive
from ._meta_store import MetaContainer, MetaStore
from ._notebook import Notebook, read_notebook, write_notebook
from ._pypackage import infer_pypackages_from_file, infer_pypackages_from_nb
from ._set_version import set_version

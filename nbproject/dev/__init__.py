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

.. autosummary::
   :toctree:

   infer_pypackages
   check_consecutiveness
   set_version

Notebook file helpers
---------------------

.. autosummary::
   :toctree:

   Notebook
   initialize_metadata
   notebook_path
   read_notebook
   write_notebook

Testing
-------

.. autosummary::
   :toctree:

   test

"""
import nbproject_test as test

from ._consecutiveness import check_consecutiveness
from ._initialize import initialize_metadata
from ._jupyter_communicate import notebook_path
from ._meta_live import MetaLive
from ._meta_store import MetaContainer, MetaStore
from ._notebook import Notebook, read_notebook, write_notebook
from ._pypackage import infer_pypackages
from ._set_version import set_version

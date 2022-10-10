import secrets
import string
from datetime import datetime, timezone
from typing import List, Optional, Union

from ._lamin_communicate import lamin_user_name, lamin_user_settings
from ._meta_store import MetaContainer
from ._notebook import Notebook


def nbproject_id():  # rename to nbproject_id also in metadata slot?
    """A 12-character base62 string."""
    # https://github.com/laminlabs/lamin-notes/blob/main/docs/2022/ids.ipynb
    base62 = string.digits + string.ascii_letters.swapcase()
    id = "".join(secrets.choice(base62) for i in range(12))
    return id


def initialize_metadata(
    nb: Optional[Notebook] = None,
    pypackage: Union[str, List[str], None] = None,
    parent: Union[str, List[str], None] = None,
) -> MetaContainer:
    """Initialize nbproject metadata.

    Args:
        nb: If a notebook is provided, also infer pypackages from the notebook.
        pypackage: One or more python packages to track.
        parent: One or more nbproject ids of direct ancestors in a notebook pipeline.
    """
    meta = MetaContainer(
        id=nbproject_id(), time_init=datetime.now(timezone.utc).isoformat()
    )

    pypackage = [pypackage] if isinstance(pypackage, str) else pypackage
    if nb is not None and isinstance(pypackage, list):
        from ._pypackage import infer_pypackages

        meta.pypackage = infer_pypackages(nb, add_pkgs=pypackage, pin_versions=True)

    if parent is not None:
        meta.parent = parent

    user_handle, user_id = lamin_user_settings()
    if user_handle is not None and user_id is not None:
        meta.user_handle = user_handle
        meta.user_id = user_id

        user_name = lamin_user_name(user_id)
        if user_name is not None:
            meta.user_name = user_name

    return meta

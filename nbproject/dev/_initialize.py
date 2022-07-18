import secrets
import string
from datetime import datetime, timezone
from typing import List, Optional, Union

from ._meta_store import MetaContainer
from ._notebook import Notebook


def nbproject_id():  # rename to nbproject_id also in metadata slot?
    """An 8-byte ID encoded as a 12-character base62 string."""
    # https://github.com/laminlabs/notes/blob/main/2022-04-04-human-friendly-ids.ipynb
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
        from ._pypackage import infer_pypackages_from_nb

        meta.pypackage = infer_pypackages_from_nb(
            nb, add_pkgs=pypackage, pin_versions=True
        )

    if parent is not None:
        meta.parent = parent

    return meta

import secrets
import string
from datetime import datetime, timezone
from typing import Optional

from ._meta_store import MetaStore
from ._notebook import Notebook


def nbproject_id():  # rename to nbproject_id also in metadata slot?
    """An 8-byte ID encoded as a 12-character base62 string."""
    # https://github.com/laminlabs/notes/blob/main/2022-04-04-human-friendly-ids.ipynb
    base62 = string.digits + string.ascii_letters.swapcase()
    id = "".join(secrets.choice(base62) for i in range(12))
    return id


def initialize_metadata(nb: Optional[Notebook] = None, dependency=False) -> MetaStore:
    """Initialize nbproject metadata.

    Args:
        nb: If a notebook is provided, also infer dependencies from the notebook.
        dependency: If `True` and `nb` provided, infer dependencies.
    """
    meta = MetaStore(
        id=nbproject_id(), time_init=datetime.now(timezone.utc).isoformat()
    )

    if nb is not None and dependency:
        from ._dependency import infer_dependencies

        meta.dependency = infer_dependencies(nb, pin_versions=True)

    return meta

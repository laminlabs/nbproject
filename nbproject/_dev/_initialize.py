import secrets
import string
from datetime import datetime, timezone
from typing import Mapping, Optional

from pydantic import BaseModel, Extra

from ._notebook import Notebook


class MetaStore(BaseModel):
    """The metadata stored in the notebook file."""

    id: str
    time_init: str
    dependency: Optional[Mapping[str, str]] = None

    class Config:  # noqa
        extra = Extra.allow


def nbproject_id():  # rename to nbproject_id also in metadata slot?
    """An 8-byte ID encoded as a 12-character base62 string."""
    # https://github.com/laminlabs/notes/blob/main/2022-04-04-human-friendly-ids.ipynb
    base62 = string.digits + string.ascii_letters.swapcase()
    id = "".join(secrets.choice(base62) for i in range(12))
    return id


def initialize_metadata(nb: Optional[Notebook]) -> MetaStore:
    """Initialize nbproject metadata.

    Args:
        nb: If a notebook is provided, also infer dependencies from the notebook.
    """
    meta = MetaStore(
        id=nbproject_id(), time_init=datetime.now(timezone.utc).isoformat()
    )

    if nb is not None:
        from ._dependency import infer_dependencies

        meta.dependency = infer_dependencies(nb, pin_versions=True)

    return meta

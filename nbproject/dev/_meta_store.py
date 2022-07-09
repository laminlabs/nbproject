from typing import Mapping, Optional

from pydantic import BaseModel, Extra


class MetaStore(BaseModel):
    """The metadata stored in the notebook file."""

    id: str
    """A universal 8-digit base62 ID."""
    time_init: str
    """Time of nbproject init in UTC. Often coincides with notebook creation."""
    dependency: Optional[Mapping[str, str]] = None
    """Dictionary of notebook dependencies and their versions."""
    version: str = "draft"
    """Published version of notebook."""

    class Config:  # noqa
        extra = Extra.allow

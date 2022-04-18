import string
import secrets
import nbformat as nbf
import pandas as pd  # mere hack for html rep
from ._logger import logger
from pydantic import BaseModel
from typing import Union
from datetime import date, datetime, timezone
from enum import Enum
from ._jupyter_communicate import notebook_path


def nbproject_uuid():  # rename to nbproject_uid also in metadata slot?
    """An 8-byte ID encoded as a 12-character base62 string."""
    # https://github.com/laminlabs/notes/blob/main/2022-04-04-human-friendly-ids.ipynb
    base62 = string.digits + string.ascii_letters.swapcase()
    uid = "".join(secrets.choice(base62) for i in range(12))
    return uid


# schema within the metadata section
class JSONSchema(BaseModel):
    nbproject_uuid: str  # a full 32 digit uuid4.hex string
    nbproject_time_init: datetime
    nbproject_time_edit: datetime


# user visible name & type configuration
class UserSchema(BaseModel):
    id: Union[
        str, int
    ] = nbproject_uuid  # the user only sees the first couple of digits
    time_init: Union[date, datetime]
    time_edit: Union[date, datetime]


# display configuration
class DisplayConf(BaseModel):
    id: int = 4  # number of digits visible, important for truncating uuid
    time_init: Enum("choice", ["date", "datetime"]) = "date"  # noqa: F821
    time_edit: Enum("choice", ["date", "datetime"]) = "date"  # noqa: F821


class Display:
    def __init__(self, nb_metadata):
        self.metadata = nb_metadata
        self.conf = DisplayConf()

    def id(self):
        """Shorten ID display."""
        return self.metadata["nbproject_uuid"][: self.conf.id]

    def time_init(self):
        """Shorten ID display."""
        dt = datetime.fromisoformat(self.metadata["nbproject_time_init"])
        if self.conf.time_init == "date":
            return dt.date()
        else:
            return dt.isoformat()  # probably something more reduced is better

    def time_edit(self):
        """Shorten ID display."""
        dt = datetime.fromisoformat(self.metadata["nbproject_time_edit"])
        if self.conf.time_edit == "date":
            return dt.date()
        else:
            return dt.isoformat()  # probably something more reduced is better


class Header:
    # filename should disappear as here but be auto-detected
    # from the jupyter notebook that calls this
    def __init__(self, filepath=None):
        if filepath is None:
            filepath = notebook_path()
            if filepath is None:
                raise RuntimeError(
                    "can't infer the name of the current notebook, "
                    "you are probably not inside a jupyter notebook"
                )
        try:
            nb = nbf.read(filepath, as_version=nbf.NO_CONVERT)
        except FileNotFoundError:
            raise RuntimeError(
                "try passing the filepath manually to nbproject.Header()"
            )
        if "nbproject_uuid" not in nb.metadata:
            logger.info(
                "to initialize nbproject: hit save, load notebook from disk ('revert')"
                " & restart"
            )
            # return string JSON-serializable string representation
            # we *do* want UUID.hex as we don't need hyphens for user intuition
            # user intuition comes through a shortened version of the hex string
            nb.metadata["nbproject_uuid"] = nbproject_uuid()
            nb.metadata["nbproject_time_init"] = datetime.now(timezone.utc).isoformat()
            nb.metadata["nbproject_time_edit"] = datetime.now(timezone.utc).isoformat()
            nbf.write(nb, filepath)
        else:
            display_ = Display(nb.metadata)
            df = pd.DataFrame(
                {
                    "id": [display_.id()],
                    "time_init": [display_.time_init()],
                    "time_edit": [display_.time_edit()],
                },
                index=[" "],
            )
            display(df.T)  # noqa

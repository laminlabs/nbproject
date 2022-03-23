import nbformat as nbf
from uuid import uuid4
import pandas as pd  # mere hack for html rep
from ._logger import logger
from pydantic import BaseModel
from typing import Union


def uuid4_hex():
    """Convert to hex string."""
    return uuid4().hex


# user visible name & type configuration
class UserSchema(BaseModel):
    id: Union[str, int] = uuid4_hex


class DisplayConf(BaseModel):
    id: int = 4  # number of digits visible, important for truncating uuid


class Display:
    def __init__(self, nb_metadata):
        self.metadata = nb_metadata
        self.conf = DisplayConf()

    def id(self):
        """Shorten ID display."""
        return self.metadata["nbproject_uuid"][: self.conf.id]


class Header:
    # filename should disappear as here but be auto-detected
    # from the jupyter notebook that calls this
    def __init__(self, filename="guide.ipynb"):
        nb = nbf.read(filename, as_version=nbf.NO_CONVERT)
        if "nbproject_uuid" not in nb.metadata:
            logger.info(
                "to initialize nbproject: hit save, load notebook from disk ('revert')"
                " & restart"
            )
            # return string JSON-serializable string representation
            # we *do* want UUID.hex as we don't need hyphens for user intuition
            # user intuition comes through a shortened version of the hex string
            nb.metadata["nbproject_uuid"] = uuid4().hex
            nbf.write(nb, filename)
        else:
            display_ = Display(nb.metadata)
            df = pd.DataFrame(
                {"id": [display_.id()]},
                index=[" "],
            )
            display(df.T)  # noqa

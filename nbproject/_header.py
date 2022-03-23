import nbformat as nbf
from uuid import uuid4
import pandas as pd  # mere hack for html rep
from ._logger import logger


class Header:
    # filename should disappear as here but be auto-detected
    # from the jupyter notebook that calls this
    def __init__(self, filename="guide.ipynb"):
        nb = nbf.read(filename, as_version=nbf.NO_CONVERT)
        if "nbproject_uuid" not in nb.metadata:
            logger.info(
                "to initialize nbproject: load notebook from disk ('revert') & restart"
            )
            # return string JSON-serializable string representation
            # we do not want UUID.hex as we want hyphens for user intuition
            nb.metadata["nbproject_uuid"] = str(uuid4())
            nbf.write(nb, filename)
        else:
            df = pd.DataFrame(
                {
                    "id": [
                        nb.metadata["nbproject_uuid"]
                    ]  # simplified key names for user display
                },
                index=[" "],
            )
            display(df.T)  # noqa

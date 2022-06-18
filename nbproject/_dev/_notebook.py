from pathlib import Path
from typing import Union

import orjson
from pydantic import BaseModel


class Notebook(BaseModel):
    metadata: dict
    nbformat: int
    nbformat_minor: int
    cells: list


def read_notebook(filepath: Union[str, Path]) -> Notebook:
    """Read a notebook from disk.

    Params
    ------
    filepath
        A path to the notebook to read.
    """
    with open(filepath, "rb") as f:
        nb = orjson.loads(f.read())

    return Notebook(**nb)


def write_notebook(nb: Notebook, filepath: Union[str, Path]):
    """Write the notebook to disk.

    Params
    ------
    nb
        Notebook to write.
    filepath
        Path where to write the notebook.
    """
    with open(filepath, "wb") as f:
        f.write(orjson.dumps(nb.dict()))

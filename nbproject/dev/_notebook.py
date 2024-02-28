from pathlib import Path
from typing import Union

import nbformat
import orjson
from pydantic import BaseModel


class Notebook(BaseModel):
    """Jupyter notebook model."""

    metadata: dict
    nbformat: int
    nbformat_minor: int
    cells: list


def read_notebook(filepath: Union[str, Path]) -> Notebook:
    """Read a notebook from disk.

    Args:
        filepath: A path to the notebook to read.
    """
    with open(filepath, "rb") as f:
        try:
            nb = orjson.loads(f.read())
        except orjson.JSONDecodeError as e:
            if "Input is a zero-length, empty document" in str(e):
                raise ValueError(
                    "Notebook cannot be empty. It must have at least a title cell."
                ) from e
            else:
                raise e

    return Notebook(**nb)


def write_notebook(nb: Notebook, filepath: Union[str, Path]):
    """Write the notebook to disk.

    Args:
        nb: Notebook to write.
        filepath: Path where to write the notebook.
    """
    nb_node = nbformat.from_dict(nb.dict())
    nbformat.write(nb_node, filepath, version=nbformat.NO_CONVERT)

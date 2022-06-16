from collections import namedtuple
from typing import Union

from ._header import Display, _filepath
from ._logger import logger
from ._notebook import Notebook, read_notebook

Meta = namedtuple("Meta", ["id", "time_init", "title", "dependency"])


def get_title(nb: Notebook) -> Union[str, None]:
    title_error = (
        "Warning: No title! Please update & save your notebook so that it has a"
        " markdown cell with the title: # My title"
    )
    if nb.cells[0]["cell_type"] != "markdown":
        logger.info(title_error)
        title = None
    else:
        title = nb.cells[0]["source"][0]
        if not title.startswith("# "):
            logger.info(title_error)
        else:
            title = title.lstrip("#").strip(" .")
    return title


def get_dependency(nb_meta: dict) -> str:
    return Display(nb_meta).dependency()


def _load_meta():
    if _filepath is None:
        return Meta(id=None, time_init=None, title=None, dependency=None)
    else:
        nb = read_notebook(_filepath)

    return Meta(
        id=nb.metadata["nbproject"]["id"],
        time_init=nb.metadata["nbproject"]["time_init"],
        title=get_title(nb),
        dependency=get_dependency(nb.metadata),
    )

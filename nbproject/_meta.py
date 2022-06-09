from collections import namedtuple
from typing import Any, Dict, List, Mapping, Union

import orjson

from ._dependency import notebook_deps
from ._header import Display

Meta = namedtuple("Meta", ["id", "time_init", "title", "dependency"])


_filepath = ""


def get_title(nb: Mapping) -> Union[str, None]:
    title_error = (
        "Warning: No title! Please update & save your notebook so that it has a"
        " markdown cell with the title: # My title"
    )
    if nb["cells"][0]["cell_type"] != "markdown":
        print(title_error)
        title = None
    else:
        title = nb["cells"][0]["source"][0]
        if not title.startswith("# "):
            print(title_error)
        else:
            title = title.lstrip("#").strip(" .")
    return title


def get_dependency(nb: Union[Dict[Any, Any], List[Any]]) -> str:
    deps = notebook_deps(nb, pin_versions=True)
    return Display().dependency(deps)


def _load_meta():
    if _filepath == "":
        return Meta(id=None, time_init=None, title=None)
    else:
        with open(_filepath, "rb") as f:
            nb = orjson.loads(f.read())

    return Meta(
        id=nb["metadata"]["nbproject"]["id"],
        time_init=nb["metadata"]["nbproject"]["time_init"],
        title=get_title(nb),
        dependency=get_dependency(nb),
    )

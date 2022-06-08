from collections import namedtuple

import orjson

Meta = namedtuple("Meta", ["id", "time_init", "title"])


_filepath = ""


def _load_meta():
    if _filepath == "":
        return Meta(id=None, time_init=None, title=None)
    else:
        with open(_filepath, "rb") as f:
            nb = orjson.loads(f.read())

    title_error = (
        "Warning: No title! Please update & save your notebook so that it has a"
        " markdown cell with the title: # My title"
    )
    if nb["cells"][0]["cell_type"] != "markdown":
        print(title_error)
        print("hello")
        title = None
    else:
        title = nb["cells"][0]["source"][0]
        if not title.startswith("# "):
            print(title_error)

    return Meta(
        id=nb["metadata"]["nbproject"]["id"],
        time_init=nb["metadata"]["nbproject"]["time_init"],
        title=title,
    )

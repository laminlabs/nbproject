from collections import namedtuple

import orjson

Meta = namedtuple("Meta", ["id", "time_init"])


_filepath = ""


def _load_meta():
    if _filepath == "":
        return Meta(id=None, time_init=None, time_run=None)
    else:
        with open(_filepath, "rb") as f:
            nb = orjson.loads(f.read())
    return Meta(
        id=nb["metadata"]["nbproject"]["id"],
        time_init=nb["metadata"]["nbproject"]["time_init"],
    )

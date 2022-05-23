import string
import secrets
import orjson
from pydantic import BaseModel
from typing import Union
from datetime import date, datetime, timezone
from enum import Enum
from textwrap import wrap
from ._logger import logger
from ._jupyter_communicate import notebook_path


def table_html(rows: list):
    html = "<table><tbody>"
    for row in rows:
        html += "<tr>"
        html += f"<td style='text-align: left;'><b>{row.pop(0)}</b></td>"
        for col in row:
            html += f"<td style='text-align: left;'>{col}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html


def display_html(html: str):
    from IPython.display import display, HTML

    display(HTML(html))


def nbproject_uid():  # rename to nbproject_uid also in metadata slot?
    """An 8-byte ID encoded as a 12-character base62 string."""
    # https://github.com/laminlabs/notes/blob/main/2022-04-04-human-friendly-ids.ipynb
    base62 = string.digits + string.ascii_letters.swapcase()
    uid = "".join(secrets.choice(base62) for i in range(12))
    return uid


# schema within the metadata section
class JSONSchema(BaseModel):
    nbproject_uid: str  # a full 32 digit uuid4.hex string
    nbproject_time_init: datetime


# user visible name & type configuration
class UserSchema(BaseModel):
    id: Union[str, int] = nbproject_uid  # the user only sees the first couple of digits
    time_init: Union[date, datetime]
    time_run: Union[date, datetime]  # not part of the ipynb metadata section


# display configuration
class DisplayConf(BaseModel):
    time_init: Enum("choice", ["date", "datetime"]) = "datetime"  # noqa: F821
    time_run: Enum("choice", ["date", "datetime"]) = "datetime"  # noqa: F821


# displays fields within the ipynb metadata section and on-the-fly computed
class Display:
    def __init__(self, nb_metadata):
        self.metadata = nb_metadata
        self.conf = DisplayConf()

    def id(self):
        """Shorten ID display."""
        uid = self.metadata["nbproject"]["uid"]
        return f"{uid[:4]}<span style='opacity:0.3'>{uid[4:]}"

    def time_init(self):
        """Shorten ID display."""
        dt = datetime.fromisoformat(self.metadata["nbproject"]["time_init"])
        if self.conf.time_init == "date":
            return dt.date()
        else:
            return dt.strftime(
                "%Y-%m-%d %H:%M"
            )  # probably something more reduced is better

    # this is not part of the ipynb metadata section
    def time_run(self, dt: datetime):
        """Shorten ID display."""
        if self.conf.time_run == "date":
            return dt.date()
        else:
            return dt.strftime(
                "%Y-%m-%d %H:%M"
            )  # probably something more reduced is better

    def dependencies(self):
        deps = None
        if "dependencies" in self.metadata["nbproject"]:
            deps = self.metadata["nbproject"]["dependencies"]
            deps = [pkg + f"=={ver}" if ver != "" else pkg for pkg, ver in deps.items()]
            deps = None if deps == [] else deps
        return deps


class Header:
    def __init__(self, filepath=None):
        if filepath is None:
            filepath = notebook_path()
            if filepath is None:
                raise RuntimeError(
                    "can't infer the name of the current notebook, "
                    "you are probably not inside a jupyter notebook"
                )
        try:
            with open(filepath, "rb") as f:
                nb = orjson.loads(f.read())
        except FileNotFoundError:
            raise RuntimeError(
                "try passing the filepath manually to nbproject.Header()"
            )
        # initialize
        if "nbproject" not in nb["metadata"]:
            logger.info(
                "To initialize nbproject for this notebook:\n* in Jupyter Lab: hit"
                " save, load notebook from disk ('revert') & restart"
            )
            nb["metadata"]["nbproject"] = {}
            nb["metadata"]["nbproject"]["uid"] = nbproject_uid()
            nb["metadata"]["nbproject"]["time_init"] = datetime.now(
                timezone.utc
            ).isoformat()

            with open(filepath, "wb") as f:
                f.write(orjson.dumps(nb))
        # read from ipynb metadata and add on-the-fly computed metadata
        else:

            display_ = Display(nb["metadata"])

            table = []
            table.append(["uid", display_.id()])
            table.append(["time_init", display_.time_init()])
            table.append(["time_run", display_.time_run(datetime.now(timezone.utc))])

            deps = display_.dependencies()
            if deps is not None:
                table.append(["dependencies", "<br>".join(wrap(", ".join(deps)))])

            display_html(table_html(table))

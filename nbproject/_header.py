import secrets
import string
from datetime import date, datetime, timezone
from enum import Enum
from textwrap import wrap
from time import sleep
from typing import Union

import orjson
from pydantic import BaseModel

from ._jupyter_communicate import notebook_path
from ._logger import logger


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
    from IPython.display import HTML, display

    display(HTML(html))


def nbproject_id():  # rename to nbproject_id also in metadata slot?
    """An 8-byte ID encoded as a 12-character base62 string."""
    # https://github.com/laminlabs/notes/blob/main/2022-04-04-human-friendly-ids.ipynb
    base62 = string.digits + string.ascii_letters.swapcase()
    id = "".join(secrets.choice(base62) for i in range(12))
    return id


# schema within the metadata section
class JSONSchema(BaseModel):
    nbproject_id: str  # a full 32 digit uid4.hex string
    nbproject_time_init: datetime


# user visible name & type configuration
class UserSchema(BaseModel):
    id: Union[str, int] = nbproject_id  # type: ignore
    time_init: Union[date, datetime]  # type: ignore
    time_run: Union[date, datetime]  # not part of the ipynb metadata section


# display configuration
class DisplayConf(BaseModel):
    time_init: Enum("choice", ["date", "datetime"]) = "datetime"  # type: ignore # noqa
    time_run: Enum("choice", ["date", "datetime"]) = "datetime"  # type: ignore # noqa


# displays fields within the ipynb metadata section and on-the-fly computed
class Display:
    def __init__(self, nb_metadata):
        self.metadata = nb_metadata
        self.conf = DisplayConf()

    def id(self):
        """Shorten ID display."""
        metadata = self.metadata["nbproject"]
        id = metadata["id"] if "id" in metadata else metadata["uid"]  # backward compat
        return f"{id[:4]}<span style='opacity:0.3'>{id[4:]}"

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

    def dependency(self):
        deps = None
        if "dependency" in self.metadata["nbproject"]:
            deps = self.metadata["nbproject"]["dependency"]
            deps = [pkg + f"=={ver}" if ver != "" else pkg for pkg, ver in deps.items()]
            deps = None if deps == [] else deps
        return deps


class Header:
    def __init__(self, filepath=None, env=None):
        filepath_env = filepath, env

        if filepath is None:
            filepath_env = notebook_path(return_env=True)
            if filepath_env is None:
                raise RuntimeError(
                    "can't infer the name of the current notebook, "
                    "you are probably not inside a jupyter notebook"
                )

        filepath = filepath_env[0]
        if env is None:
            env = filepath_env[1]

        try:
            with open(filepath, "rb") as f:
                nb = orjson.loads(f.read())
        except FileNotFoundError:
            raise RuntimeError(
                "try passing the filepath manually to nbproject.Header()"
            )
        # initialize
        if "nbproject" not in nb["metadata"]:
            from ._dependency import notebook_deps

            logger.info(
                "To initialize nbproject for this notebook:\n* In Jupyter Lab: hit"
                " restart when asked!"
            )

            if env == "lab":
                from ipylab import JupyterFrontEnd

                app = JupyterFrontEnd()
                # ensure that all user edits are saved before the
                # notebook will be loaded by the backend
                app.commands.execute("docmanager:save")
                # it's important that the frontend is done saving
                # before the backend loads
                sleep(1)

            # now load the notebook with the backend
            with open(filepath, "rb") as f:
                nb = orjson.loads(f.read())
            # write metadata from the backend
            nb["metadata"]["nbproject"] = {}
            nb["metadata"]["nbproject"]["id"] = nbproject_id()
            nb["metadata"]["nbproject"]["time_init"] = datetime.now(
                timezone.utc
            ).isoformat()
            nb["metadata"]["nbproject"]["dependency"] = notebook_deps(
                nb, pin_versions=True
            )

            # write the file from the backend
            with open(filepath, "wb") as f:
                f.write(orjson.dumps(nb))

            if env == "lab":
                # reload the notebook with metadata by the frontend
                # otherwise Jupyter lab notices the mismatch
                # and shows a confusing dialogue
                app.commands.execute("docmanager:reload")
                # restart and re-execute `from nbproject import header`
                app.commands.execute("notebook:restart-and-run-to-selected")
        # read from ipynb metadata and add on-the-fly computed metadata
        else:

            # display metadata
            display_ = Display(nb["metadata"])

            time_run = display_.time_run(datetime.now(timezone.utc))

            table = []
            table.append(["id", display_.id()])
            table.append(["time_init", display_.time_init()])
            table.append(["time_run", time_run])

            deps = display_.dependency()
            if deps is not None:
                table.append(["dependency", "<br>".join(wrap(", ".join(deps)))])

            display_html(table_html(table))

        # make filepath available through API
        import nbproject._meta

        nbproject._meta._filepath = filepath

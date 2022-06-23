from datetime import date, datetime, timezone
from enum import Enum
from time import sleep
from typing import Mapping

from pydantic import BaseModel

from ._logger import logger
from .dev._initialize import initialize_metadata
from .dev._jupyter_communicate import notebook_path
from .dev._notebook import read_notebook, write_notebook

_filepath = None
_time_run = None


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


# display configuration
class DisplayConf(BaseModel):
    time_init: Enum("choice", ["date", "datetime"]) = "datetime"  # type: ignore # noqa
    time_run: Enum("choice", ["date", "datetime"]) = "datetime"  # type: ignore # noqa


# displays fields within the ipynb metadata section and on-the-fly computed
class Display:
    def __init__(self, nb_metadata=None):
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

    def dependency(self, deps: Mapping = None):
        if deps is None and "dependency" in self.metadata["nbproject"]:
            deps = self.metadata["nbproject"]["dependency"]

        if deps is None:
            return None

        deps_list = []
        for pkg, ver in deps.items():
            if ver != "":
                deps_list.append(pkg + f"=={ver}")
            else:
                deps_list.append(pkg)

        if deps_list == []:
            return None
        else:
            return deps_list


class Header:
    """Metadata header class.

    An object of this class displays nbproject metadata fields
    for the current notebook on initialization. If the notebook doesn't have
    nbproject metadata, it will be initialized and written to the notebook.
    """

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
            nb = read_notebook(filepath)
        except FileNotFoundError:
            raise RuntimeError(
                "try passing the filepath manually to nbproject.Header()"
            )
        # initialize
        if "nbproject" not in nb.metadata:
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
                nb = read_notebook(filepath)

            # write metadata from the backend
            nb.metadata["nbproject"] = initialize_metadata(nb).dict()

            # write the file from the backend
            write_notebook(nb, filepath)

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
            display_ = Display(nb.metadata)

            time_run = datetime.now(timezone.utc)

            # make time_run available through API
            global _time_run
            _time_run = time_run

            table = []
            table.append(["id", display_.id()])
            table.append(["time_init", display_.time_init()])
            table.append(["time_run", display_.time_run(time_run)])

            deps_display = display_.dependency()
            if deps_display is not None:
                table.append(["dependency", " ".join(deps_display)])

            display_html(table_html(table))

        # make filepath available through API
        global _filepath
        _filepath = filepath

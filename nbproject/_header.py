from datetime import date, datetime, timezone
from enum import Enum
from typing import Mapping

from pydantic import BaseModel

from ._logger import logger
from .dev._dependency import infer_dependencies_from_nb
from .dev._initialize import initialize_metadata
from .dev._jupyter_communicate import notebook_path
from .dev._jupyter_lab_commands import _reload_and_restart_notebook, _save_notebook
from .dev._notebook import read_notebook, write_notebook

_filepath = None
_env = None
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
class DisplayMeta:
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

    def version(self):
        if "version" in self.metadata["nbproject"]:
            return self.metadata["nbproject"]["version"]
        else:
            return "draft"  # for backward-compat right now

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
            deps_list.sort()
            return deps_list


def header(filepath=None, env=None):
    """Display metadata and start tracking.

    - Displays nbproject metadata fields for the current notebook.
    - If the notebook has no nbproject metadata, initializes & writes metadata to disk.
    - Starts tracking dependencies.
    """
    filepath_env = filepath, env

    if filepath is None:
        filepath_env = notebook_path(return_env=True)
        if filepath_env is None:
            logger.info(
                "Can't infer the name of the current notebook, "
                "you are probably not inside a Jupyter notebook. "
                "Please call `header(filepath='your-file.ipynb')`."
            )
            return None
        filepath = filepath_env[0]

    if env is None:
        env = filepath_env[1]
    # This is a quirk we run into when passing filepath manually!
    # We just assume jupyter lab as an environment for now
    if env is None:
        env = "lab"
        logger.info("Assuming editor is Jupyter Lab.")

    try:
        nb = read_notebook(filepath)
    except FileNotFoundError:
        raise RuntimeError("Try passing the filepath manually to nbproject.Header().")
    # initialize
    if "nbproject" not in nb.metadata:
        if env == "lab":
            msg = "Hit the restart button when asked."
        else:
            msg = (
                "Hit save & reload from disk, i.e, *discard* editor content. If you do"
                " not want to lose editor changes, hit save *before* running"
                " `header()`. Consider using Jupyter Lab for a seamless interactive"
                " experience."
            )
        logging_message = f"To initialize nbproject: {msg}"
        logger.info(logging_message)

        if env == "lab":
            _save_notebook()
            nb = read_notebook(filepath)

        # write metadata from the backend
        nb.metadata["nbproject"] = initialize_metadata(nb).dict()

        # write the file from the backend
        write_notebook(nb, filepath)

        if env == "lab":
            # reload the notebook with metadata by the frontend
            # otherwise Jupyter lab notices the mismatch
            # and shows a confusing dialogue
            _reload_and_restart_notebook()
        else:
            raise SystemExit(f"Init complete. {msg}")

    # read from ipynb metadata and add on-the-fly computed metadata
    else:
        # display metadata
        dm = DisplayMeta(nb.metadata)

        time_run = datetime.now(timezone.utc)

        # make time_run available through API
        global _time_run
        _time_run = time_run

        table = []
        table.append(["id", dm.id()])
        table.append(["time_init", dm.time_init()])
        table.append(["time_run", dm.time_run(time_run)])

        version = dm.version()
        table.append(["version", version])

        dep_store = dm.dependency()
        add_pkgs = None

        if dep_store is not None:
            # only display stored dependencies for published notebooks
            # for draft notebooks, they have little meaning
            if version != "draft":
                table.append(["dependency_store", " ".join(dep_store)])
            add_pkgs = [pkg.partition("==")[0] for pkg in dep_store]

        dep_live = dm.dependency(
            infer_dependencies_from_nb(nb, add_pkgs, pin_versions=True)
        )
        if dep_live is not None:
            suffix = "" if version == "draft" else "_live"
            table.append([f"dependency{suffix}", " ".join(dep_live)])

        display_html(table_html(table))

        # make filepath available through API
        global _filepath
        global _env

        _filepath = filepath
        _env = env

from datetime import date, datetime, timezone
from enum import Enum
from typing import Mapping, Optional

from pydantic import BaseModel

from .._logger import logger
from ._consecutiveness import check_consecutiveness
from ._notebook import Notebook
from ._pypackage import infer_pypackages_from_nb


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


def color_id(id: str):
    return f"{id[:4]}<span style='opacity:0.3'>{id[4:]}</span>"


# displays fields within the ipynb metadata section and on-the-fly computed
class DisplayMeta:
    def __init__(self, metadata: Mapping):
        self.metadata = metadata
        self.conf = DisplayConf()

    def id(self):
        """Shorten ID display."""
        id = self.metadata["id"] if "id" in self.metadata else self.metadata["uid"]
        return color_id(id)

    def version(self):
        return self.metadata["version"]

    def parent(self):
        if "parent" in self.metadata:
            parent = self.metadata["parent"]
            if parent is None:
                return None
            if isinstance(parent, list):
                return " ".join([color_id(id) for id in parent])
            else:
                return color_id(parent)
        else:
            return None

    def time_init(self):
        """Shorten ID display."""
        dt = datetime.fromisoformat(self.metadata["time_init"])
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

    def pypackage(self, deps: Optional[Mapping] = None):
        if deps is None and "pypackage" in self.metadata:
            deps = self.metadata["pypackage"]

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


def table_metadata(
    metadata: Mapping, notebook: Notebook, time_run: Optional[datetime] = None
):
    dm = DisplayMeta(metadata)

    table = []
    table.append(["id", dm.id()])
    version = dm.version()
    table.append(["version", version])
    table.append(["time_init", dm.time_init()])

    if time_run is None:
        time_run = datetime.now(timezone.utc)
    table.append(["time_run", dm.time_run(time_run)])

    if dm.parent() is not None:
        table.append(["parent", dm.parent()])

    if version != "draft":
        logger.disable("nbproject.dev._consecutiveness")
        consecutiveness = check_consecutiveness(notebook)
        logger.enable("nbproject.dev._consecutiveness")

        table.append(["consecutive_cells", str(consecutiveness)])

    dep_store = dm.pypackage()
    if dep_store is not None:
        add_pkgs = [pkg.partition("==")[0] for pkg in dep_store]
    else:
        add_pkgs = None
    dep_live = dm.pypackage(
        infer_pypackages_from_nb(notebook, add_pkgs, pin_versions=True)
    )

    # simplify display when stored & live pypackages match
    if dep_store is not None and dep_live is not None and dep_live == dep_store:
        table.append(["pypackage", " ".join(dep_store)])
    else:
        if dep_store is not None:
            table.append(["pypackage_store", " ".join(dep_store)])
            suffix = "_live"
        else:
            suffix = ""
        if dep_live is not None:
            table.append([f"pypackage{suffix}", " ".join(dep_live)])

    return table_html(table)

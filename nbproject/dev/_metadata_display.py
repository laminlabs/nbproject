from datetime import date, datetime, timezone
from enum import Enum
from typing import Mapping, Optional

from pydantic import BaseModel

from .._logger import logger
from ._consecutiveness import check_consecutiveness
from ._dependency import infer_dependencies_from_nb
from ._notebook import Notebook


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
    def __init__(self, metadata: Mapping):
        self.metadata = metadata
        self.conf = DisplayConf()

    def id(self):
        """Shorten ID display."""
        id = self.metadata["id"] if "id" in self.metadata else self.metadata["uid"]
        return f"{id[:4]}<span style='opacity:0.3'>{id[4:]}"

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

    def version(self):
        if "version" in self.metadata:
            return self.metadata["version"]
        else:
            return "draft"  # for backward-compat right now

    def dependency(self, deps: Optional[Mapping] = None):
        if deps is None and "dependency" in self.metadata:
            deps = self.metadata["dependency"]

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
    table.append(["time_init", dm.time_init()])

    if time_run is None:
        time_run = datetime.now(timezone.utc)
    table.append(["time_run", dm.time_run(time_run)])

    version = dm.version()
    table.append(["version", version])

    if version != "draft":
        logger.disable("nbproject.dev._consecutiveness")
        consecutiveness = check_consecutiveness(notebook)
        logger.enable("nbproject.dev._consecutiveness")

        table.append(["consecutive_cells", str(consecutiveness)])

    dep_store = dm.dependency()
    if dep_store is not None:
        add_pkgs = [pkg.partition("==")[0] for pkg in dep_store]
    else:
        add_pkgs = None
    dep_live = dm.dependency(
        infer_dependencies_from_nb(notebook, add_pkgs, pin_versions=True)
    )

    # simplify display when stored & live dependencies match
    if dep_store is not None and dep_live is not None and dep_live == dep_store:
        table.append(["dependency", " ".join(dep_store)])
    else:
        if dep_store is not None:
            table.append(["dependency_store", " ".join(dep_store)])
            suffix = "_live"
        else:
            suffix = ""
        if dep_live is not None:
            table.append([f"dependency{suffix}", " ".join(dep_live)])

    return table_html(table)

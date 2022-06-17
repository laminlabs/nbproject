from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union

from ._dev._initialize import Metadata
from ._dev._integrity import check_integrity
from ._dev._jupyter_communicate import notebook_path
from ._dev._notebook import Notebook, read_notebook
from ._header import _filepath, _time_run
from ._logger import logger


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
            title = None
        else:
            title = title.lstrip("#").strip(" .")
    return title


class Live:
    def __init__(self, nb_path: Union[str, Path], time_run: Optional[datetime] = None):
        self._nb_path = nb_path
        self._time_run = time_run

    @property
    def title(self):
        nb = read_notebook(self._nb_path)
        return get_title(nb)

    @property
    def dependency(self):
        from ._dev._dependency import infer_dependencies

        nb = read_notebook(self._nb_path)
        return infer_dependencies(nb, pin_versions=True)

    @property
    def integrity(self):
        logger.info("Save the notebook before running the integrity check.")
        nb = read_notebook(self._nb_path)
        return check_integrity(nb, ignore_code=".live.integrity")

    @property
    def time_run(self):
        if self._time_run is None:
            self._time_run = datetime.now(timezone.utc)
        return self._time_run.isoformat()

    @property
    def time_passed(self):
        return (datetime.now(timezone.utc) - self._time_run).total_seconds()

    def __repr__(self):
        return " ".join([key for key in dir(self) if key[0] != "_"])


class Meta:
    def __init__(self, filepath, time_run):
        if filepath is None:
            filepath = notebook_path()

        self._live = Live(filepath, time_run)

        nb_meta = read_notebook(filepath).metadata
        if "nbproject" in nb_meta:
            self._store = Metadata(**nb_meta["nbproject"])
        else:
            self._store = None

    @property
    def live(self):
        return self._live

    @property
    def store(self):
        return self._store

    def __repr__(self):
        return (
            "Metadata object with .live and .store metadata fields:\n"
            f"  .store: {self.store}\n"
            f"  .live: {self.live}"
        )


meta = Meta(_filepath, _time_run)

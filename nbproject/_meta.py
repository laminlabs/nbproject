from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union

from ._logger import logger
from .dev._initialize import MetaStore
from .dev._integrity import check_integrity
from .dev._jupyter_communicate import notebook_path
from .dev._notebook import Notebook, read_notebook, write_notebook


def get_title(nb: Notebook) -> Optional[str]:
    """Get title of the notebook."""
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


class MetaLive:
    """Live properties of the notebook.

    All attributes represent either the execution information or properties inferred
    on access from the notebook's content.
    """

    def __init__(self, nb_path: Union[str, Path], time_run: Optional[datetime] = None):
        self._nb_path = nb_path
        self._time_run = time_run

    @property
    def title(self):
        """Get the title of the notebook.

        The first cell should contain markdown text formatted as a title.
        """
        nb = read_notebook(self._nb_path)
        return get_title(nb)

    @property
    def dependency(self):
        """Infer dependencies for the notebook on access."""
        from .dev._dependency import infer_dependencies

        nb = read_notebook(self._nb_path)
        add_pkgs = None
        if "nbproject" in nb.metadata and "dependency" in nb.metadata["nbproject"]:
            add_pkgs = nb.metadata["nbproject"]["dependency"].keys()
        return infer_dependencies(nb, add_pkgs, pin_versions=True)

    @property
    def integrity(self):
        """Check integrity of the notebook.

        The notebook should be saved before accessing this attribute.
        """
        logger.info("Save the notebook before running the integrity check.")
        nb = read_notebook(self._nb_path)
        return check_integrity(nb, ignore_code=".live.integrity")

    @property
    def time_run(self):
        """The time when the current session started.

        To get the proper time run, you need to use `from nbproject import header`
        at the beginning of the notebook. Otherwise, the time run is set to the time
        of the first access to this attribute.
        """
        if self._time_run is None:
            self._time_run = datetime.now(timezone.utc)
        return self._time_run.isoformat()

    @property
    def time_passed(self):
        """Number of seconds elapsed from `time_run`."""
        return (datetime.now(timezone.utc) - self._time_run).total_seconds()

    def __repr__(self):
        return " ".join([key for key in dir(self) if key[0] != "_"])


class Meta:
    """Access live and stored metadata.

    A metadata object has the `store` attribute to access the nbproject metadata
    of the notebook and `live` for the execution info and properties
    derived from the notebook's content.
    """

    def __init__(self, filepath, time_run):
        if filepath is None:
            filepath = notebook_path()

        self._filepath = filepath

        self._live = MetaLive(filepath, time_run)

        nb_meta = read_notebook(filepath).metadata
        if "nbproject" in nb_meta:
            self._store = MetaStore(**nb_meta["nbproject"])
        else:
            self._store = None

    @property
    def store(self) -> Optional[MetaStore]:
        """Metadata stored in the notebook."""
        return self._store

    @property
    def live(self) -> MetaLive:
        """Contains execution info and properties of the notebook content."""
        return self._live

    def write(self):
        """Write nbproject metadata in `.store` to the current file.

        You can edit the nbproject metadata of the current notebook
        by changing `.store` fields and then using this function
        to write the changes to the file. Save the notebook before writing.
        """
        logger.info("Restart the notebook.")
        nb = read_notebook(self._filepath)
        nb.metadata["nbproject"] = self.store.dict()
        write_notebook(nb, self._filepath)

    def __repr__(self):
        return (
            "Metadata object with .live and .store metadata fields:\n"
            f"  .store: {self.store}\n"
            f"  .live: {self.live}"
        )


def _load_meta():
    from ._header import _filepath, _time_run

    meta = Meta(_filepath, _time_run)
    return meta

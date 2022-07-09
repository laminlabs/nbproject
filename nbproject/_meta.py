from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union

from ._logger import logger
from .dev._integrity import check_integrity
from .dev._jupyter_communicate import notebook_path
from .dev._jupyter_lab_commands import _save_notebook
from .dev._meta_store import MetaContainer, MetaStore
from .dev._notebook import Notebook, read_notebook


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

    def __init__(
        self,
        nb_path: Union[str, Path],
        time_run: Optional[datetime] = None,
        env: Optional[str] = None,
    ):
        self._nb_path = nb_path
        self._env = env
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
        from .dev._dependency import infer_dependencies_from_file

        return infer_dependencies_from_file(self._nb_path)

    @property
    def integrity(self):
        """Compute integrity of the notebook.

        Returns those cell transitions that violate execution at increments of 1
        as a list of tuples.
        """
        if self._env == "lab":
            _save_notebook()
        elif self._env != "test":
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

    def __init__(self, filepath, time_run, env):
        filepath_env = filepath, env

        if filepath is None:
            filepath_env = notebook_path(return_env=True)

            if filepath_env is None:
                filepath_env = None, None

            filepath = filepath_env[0]

        if env is None:
            env = filepath_env[1]

        self._filepath = filepath
        self._env = env

        self._live = MetaLive(filepath, time_run, env)

        if self._filepath is not None:
            nb_meta = read_notebook(filepath).metadata
        else:
            logger.warning("You are probably not inside a jupyter notebook.")
            nb_meta = None

        if nb_meta is not None and "nbproject" in nb_meta:
            meta_container = MetaContainer(**nb_meta["nbproject"])
        else:
            empty = "not initialized"
            meta_container = MetaContainer(id=empty, time_init=empty, version=empty)

        self._store = MetaStore(meta_container, filepath, env)

    @property
    def store(self) -> MetaStore:
        """Metadata stored in the notebook."""
        return self._store

    @property
    def live(self) -> MetaLive:
        """Contains execution info and properties of the notebook content."""
        return self._live

    def __repr__(self):
        return (
            "Metadata object with .live and .store metadata fields:\n"
            f"  .store: {self.store}\n"
            f"  .live: {self.live}"
        )


def _load_meta():
    from ._header import _env, _filepath, _time_run

    meta = Meta(_filepath, _time_run, _env)
    return meta

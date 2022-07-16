from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union

from ._logger import logger
from .dev._consecutiveness import check_consecutiveness
from .dev._jupyter_communicate import notebook_path
from .dev._jupyter_lab_commands import _save_notebook
from .dev._meta_store import MetaContainer, MetaStore
from .dev._notebook import Notebook, read_notebook


def get_title(nb: Notebook) -> Optional[str]:
    """Get title of the notebook."""
    if nb.cells[0]["cell_type"] != "markdown":
        title = None
    else:
        title = nb.cells[0]["source"][0]
        if not title.startswith("# "):
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
    def title(self) -> Optional[str]:
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
    def consecutive_cells(self) -> bool:
        """Have notebook cells been consecutively executed?

        Logs cell transitions that violate execution at increments of 1
        as a list of tuples.
        """
        if self._env == "lab":
            _save_notebook()
        elif self._env != "test":
            logger.info("Save the notebook before checking for consecutiveness.")
        nb = read_notebook(self._nb_path)
        violations = check_consecutiveness(
            nb, calling_statement=".live.consecutive_cells"
        )
        if len(violations) > 0:
            return False
        else:
            return True

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


class meta:
    """Access live and stored metadata.

    A metadata object has the `store` attribute to access the nbproject metadata
    of the notebook and `live` for the execution info and properties
    derived from the notebook's content.
    """

    _filepath: Union[str, Path, None] = None
    _env = None
    _time_run = None
    _store: Union[MetaStore, None] = None
    _live: Union[MetaLive, None] = None

    @classmethod
    def _get_env(cls):
        from ._header import _env, _filepath, _time_run

        env = _env
        filepath = _filepath
        filepath_env = _filepath, _env

        if filepath is None:
            filepath_env = notebook_path(return_env=True)
            if filepath_env is None:
                filepath_env = None, None
            filepath = filepath_env[0]

        if env is None:
            env = filepath_env[1]

        cls._filepath = _filepath
        cls._env = env
        cls._time_run = _time_run

    @classmethod
    @property
    def store(cls) -> MetaStore:
        """Metadata stored in the notebook."""
        if cls._store is None:
            cls._get_env()
            nb_meta = read_notebook(cls._filepath).metadata  # type: ignore

            if nb_meta is not None and "nbproject" in nb_meta:
                meta_container = MetaContainer(**nb_meta["nbproject"])
            else:
                empty = "not initialized"
                meta_container = MetaContainer(id=empty, time_init=empty, version=empty)
            cls._store = MetaStore(meta_container, cls._filepath, cls._env)
        return cls._store

    @classmethod
    @property
    def live(cls) -> MetaLive:
        """Contains execution info and properties of the notebook content."""
        if cls._live is None:
            cls._get_env()
            cls._live = MetaLive(cls._filepath, cls._time_run, cls._env)  # type: ignore
        return cls._live

    def __repr__(self):
        return (
            "Metadata object with .live and .store metadata fields:\n"
            f"  .store: {self.store}\n"
            f"  .live: {self.live}"
        )

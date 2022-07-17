from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union

from .._logger import logger
from ._consecutiveness import check_consecutiveness
from ._jupyter_lab_commands import _save_notebook
from ._notebook import Notebook, read_notebook


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
    def pypackage(self):
        """Infer pypackages for the notebook on access."""
        from ._pypackage import infer_pypackages_from_file

        return infer_pypackages_from_file(self._nb_path)

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
        consecutiveness = check_consecutiveness(
            nb, calling_statement=".live.consecutive_cells"
        )
        return consecutiveness

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
        return "Fields: " + " ".join([key for key in dir(self) if key[0] != "_"])

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union

from nbproject._logger import logger

from ._consecutiveness import check_consecutiveness
from ._jupyter_lab_commands import _save_notebook
from ._lamin_communicate import lamin_user_settings
from ._notebook import Notebook, read_notebook
from ._pypackage import infer_pypackages


def get_title(nb: Notebook) -> Optional[str]:
    """Get title of the notebook."""
    # loop through all cells
    for cell in nb.cells:
        # only consider markdown
        if cell["cell_type"] == "markdown":
            # grab source
            text = cell["source"][0]
            # loop through lines
            for line in text.split("\n"):
                # if finding a level-1 heading, consider it a title
                if line.startswith("# "):
                    title = line.lstrip("#").strip(" .").strip("\n")
                    return title
    return None


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
        """Infer pypackages for the notebook.

        This accounts for additional pypackages in the file metadata.
        """
        nb = read_notebook(self._nb_path)
        add_pkgs = None
        if "nbproject" in nb.metadata and "pypackage" in nb.metadata["nbproject"]:
            if nb.metadata["nbproject"]["pypackage"] is not None:
                add_pkgs = nb.metadata["nbproject"]["pypackage"].keys()
        return infer_pypackages(nb, add_pkgs, pin_versions=True)

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

    @property
    def user_handle(self):
        """User handle from lamindb."""
        return lamin_user_settings().handle

    @property
    def user_id(self):
        """User ID from lamindb."""
        return lamin_user_settings().id

    @property
    def user_name(self):
        """User name from lamindb."""
        return lamin_user_settings().name

    def __repr__(self):
        return "Fields: " + " ".join([key for key in dir(self) if key[0] != "_"])

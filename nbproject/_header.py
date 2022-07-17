from datetime import datetime, timezone
from typing import Optional

from ._logger import logger
from .dev._initialize import initialize_metadata
from .dev._jupyter_communicate import notebook_path
from .dev._jupyter_lab_commands import _reload_notebook, _save_notebook
from .dev._metadata_display import display_html, table_metadata
from .dev._notebook import read_notebook, write_notebook

_filepath = None
_env = None
_time_run = None


def header(filepath: Optional[str] = None, env: Optional[str] = None):
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
        nb = read_notebook(filepath)  # type: ignore
    except FileNotFoundError:
        raise RuntimeError("Try passing the filepath manually to nbproject.Header().")
    # initialize
    if "nbproject" not in nb.metadata:
        logger.info("Initializing.")

        if env == "lab":
            _save_notebook()
            nb = read_notebook(filepath)  # type: ignore

        nb.metadata["nbproject"] = initialize_metadata(nb).dict()
        write_notebook(nb, filepath)  # type: ignore

        if env == "lab":
            _reload_notebook()
        else:
            logging_message = (
                "Hit save & reload from disk, i.e, *discard* editor content. If you do"
                " not want to lose editor changes, hit save *before* running"
                " `header()`. Consider using Jupyter Lab for a seamless interactive"
                " experience."
            )
            raise SystemExit(f"Init complete. {logging_message}")

    # read from ipynb metadata and add on-the-fly computed metadata
    else:
        # make time_run available through API
        time_run = datetime.now(timezone.utc)

        global _time_run
        _time_run = time_run

        logger.disable("nbproject.dev._consecutiveness")

        table = table_metadata(nb.metadata["nbproject"], nb, time_run)
        display_html(table)

        logger.enable("nbproject.dev._consecutiveness")

        # make filepath available through API
        global _filepath
        global _env

        _filepath = filepath
        _env = env

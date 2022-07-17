from datetime import datetime, timezone
from typing import Union

from ._logger import logger
from .dev._initialize import initialize_metadata
from .dev._jupyter_communicate import notebook_path
from .dev._jupyter_lab_commands import _reload_notebook, _save_notebook
from .dev._metadata_display import display_html, table_metadata
from .dev._notebook import read_notebook, write_notebook

_filepath = None
_env = None
_time_run = None


def header(
    *,
    parent: Union[str, list[str], None] = None,
    filepath: Union[str, None] = None,
    env: Union[str, None] = None,
):
    """Display metadata and start tracking dependencies.

    If the notebook has no nbproject metadata, initializes & writes metadata to disk.

    Args:
        parent: One or more nbproject ids of direct ancestors in a notebook pipeline.
        filepath: Filepath of notebook. Only needed if automatic inference fails.
        env: Editor environment. Only needed if automatic inference fails.
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
    # The following occurs when passing filepath manually
    # We assume Jupyter Lab as an environment for now
    if env is None:
        env = "lab"
        logger.info("Assuming editor is Jupyter Lab.")

    try:
        nb = read_notebook(filepath)  # type: ignore
    except FileNotFoundError:
        raise RuntimeError("Try passing the filepath manually to nbproject.Header().")

    # make time_run available through API
    time_run = datetime.now(timezone.utc)
    global _time_run, _filepath, _env
    _time_run, _filepath, _env = time_run, filepath, env

    # initialize
    if "nbproject" not in nb.metadata:
        logger.info("Initializing.")

        if env == "lab":
            _save_notebook()
            nb = read_notebook(filepath)  # type: ignore

        nb.metadata["nbproject"] = initialize_metadata(nb).dict()
        write_notebook(nb, filepath)  # type: ignore

        if parent is not None:
            from nbproject import meta

            meta.store.parent = parent
            meta.store.write()

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
        table = table_metadata(nb.metadata["nbproject"], nb, time_run)
        display_html(table)

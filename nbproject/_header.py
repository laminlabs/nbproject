from datetime import datetime, timezone
from typing import List, Union

from ._logger import logger
from .dev._initialize import initialize_metadata
from .dev._jupyter_communicate import notebook_path
from .dev._jupyter_lab_commands import _reload_notebook, _save_notebook
from .dev._metadata_display import display_html, table_metadata
from .dev._notebook import read_notebook, write_notebook

_filepath = None
_env = None
_time_run = None


msg_init_complete = (
    "Init complete. Hit save & reload from disk, i.e, *discard* editor content. If you"
    " do not want to lose editor changes, hit save *before* running `header()`."
    " Consider using Jupyter Lab for a seamless interactive experience."
)

msg_inconsistent_parent = (
    "Argument parent is inconsistent with store.\nPlease update"
    " metadata, e.g.: meta.store.parent = parent; meta.store.write()"
)


def msg_inconsistent_pypackage(pypackage):
    return (
        "Argument pypackage is inconsistent with metadata store.\nPlease update"
        f' metadata: meta.store.add_pypackages("{pypackage}"); meta.store.write()'
    )


def header(
    *,
    parent: Union[str, List[str], None] = None,
    pypackage: Union[str, List[str], None] = None,
    filepath: Union[str, None] = None,
    env: Union[str, None] = None,
):
    """Display metadata and start tracking dependencies.

    If the notebook has no nbproject metadata, initializes & writes metadata to disk.

    Args:
        parent: One or more nbproject ids of direct ancestors in a notebook pipeline.
        pypackage: One or more python packages to track.
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

        nb.metadata["nbproject"] = initialize_metadata(
            nb, parent=parent, pypackage=pypackage
        ).dict()
        write_notebook(nb, filepath)  # type: ignore

        if env == "lab":
            _reload_notebook()
        else:
            raise SystemExit(msg_init_complete)

    # read from ipynb metadata and add on-the-fly computed metadata
    else:
        metadata = nb.metadata["nbproject"]
        table = table_metadata(metadata, nb, time_run)
        display_html(table)

        # check whether updates to init are needed
        if parent is not None:
            if "parent" not in metadata:
                logger.info(msg_inconsistent_parent)
            elif metadata["parent"] != parent:
                logger.info(msg_inconsistent_parent)
        if pypackage is not None:
            pypackage = [pypackage] if isinstance(pypackage, str) else pypackage
            if "pypackage" not in metadata or metadata["pypackage"] is None:
                logger.info(msg_inconsistent_pypackage(pypackage[0]))
            else:
                for pkg in pypackage:
                    if pkg not in metadata["pypackage"]:
                        logger.info(msg_inconsistent_pypackage(pypackage))

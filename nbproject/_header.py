import re
from datetime import datetime, timezone
from typing import List, Mapping, Optional, Tuple, Union

from ._logger import logger
from .dev._frontend_commands import _reload_notebook, _save_notebook
from .dev._initialize import initialize_metadata
from .dev._jupyter_communicate import notebook_path
from .dev._metadata_display import display_html, table_metadata
from .dev._notebook import Notebook, read_notebook, write_notebook

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
        f' metadata: meta.store.add_pypackages("{pypackage}").write()'
    )


def _output_table(notebook: Notebook, table: str):
    out = {
        "data": {
            "text/html": [table],
            "text/plain": ["<IPython.core.display.HTML object>"],
        },
        "metadata": {},
        "output_type": "display_data",
    }

    header_re = re.compile(r"^[^#]*header\(", flags=re.MULTILINE)
    ccount = 0
    for cell in notebook.cells:
        if cell["cell_type"] != "code":
            continue
        elif cell["execution_count"] is not None:
            ccount = cell["execution_count"]

        if header_re.match("".join(cell["source"])) is not None:
            cell["outputs"] = [out]
            cell["execution_count"] = ccount + 1
            # update only once
            break


def header(
    *,
    parent: Union[str, List[str], None] = None,
    pypackage: Union[str, List[str], None] = None,
    filepath: Union[str, None] = None,
    env: Union[str, None] = None,
    metadata_only: bool = False,
) -> Optional[Tuple[Mapping, bool, Notebook]]:
    """Display metadata and start tracking dependencies.

    If the notebook has no nbproject metadata, initializes & writes metadata to disk.

    Args:
        parent: One or more nbproject ids of direct ancestors in a notebook pipeline.
        pypackage: One or more python packages to track.
        filepath: Filepath of notebook. Only needed if automatic inference fails.
        env: Editor environment. Only needed if automatic inference fails.
            Pass `'lab'` for jupyter lab and `'notebook'` for jupyter notebook,
            this can help to identify the correct mechanism for interactivity
            when automatic inference fails.
        metadata_only: Whether or not to return only metadata
            without writing or displaying anything.
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
        # this logs "jupyter lab" in vscode and hence, is confusing
        # logger.info("Assuming editor is Jupyter Lab.")

    try:
        nb = read_notebook(filepath)  # type: ignore
    except FileNotFoundError:
        raise RuntimeError(
            "Try passing the filepath manually to nbproject.Header()."
        ) from None

    # make time_run available through API
    time_run = datetime.now(timezone.utc)
    global _time_run, _filepath, _env
    _time_run, _filepath, _env = time_run, filepath, env

    # initialize
    if "nbproject" not in nb.metadata:
        logger.info("Attaching notebook metadata")

        if env in ("lab", "notebook"):
            _save_notebook(env)
            nb = read_notebook(filepath)  # type: ignore

        metadata = initialize_metadata(nb, parent=parent, pypackage=pypackage).dict()

        if metadata_only:
            # True here means that the metdata has been initialized now
            return metadata, True, nb
        else:
            nb.metadata["nbproject"] = metadata
            _output_table(nb, table_metadata(metadata, nb, time_run))
            write_notebook(nb, filepath)  # type: ignore

            if env in ("lab", "notebook"):
                _reload_notebook(env)
            else:
                raise SystemExit(msg_init_complete)

    # read from ipynb metadata and add on-the-fly computed metadata
    else:
        metadata = nb.metadata["nbproject"]
        if not metadata_only:
            table = table_metadata(metadata, nb, time_run)
            display_html(table)

        # check whether updates to init are needed
        if parent is not None:
            if "parent" not in metadata or metadata["parent"] != parent:
                logger.info(msg_inconsistent_parent)
        if pypackage is not None:
            pypackage = [pypackage] if isinstance(pypackage, str) else pypackage
            is_empty = "pypackage" not in metadata or metadata["pypackage"] is None
            for pkg in pypackage:
                if is_empty or pkg not in metadata["pypackage"]:
                    logger.info(msg_inconsistent_pypackage(pkg))

        if metadata_only:
            # False here means that the notebook has the metadata already
            return metadata, False, nb

    return None

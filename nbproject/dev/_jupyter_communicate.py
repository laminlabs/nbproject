import os
import sys
from itertools import chain
from pathlib import Path, PurePath
from urllib import request

import orjson

from nbproject._logger import logger

from ._jupyter_lab_commands import _ipylab_is_installed, _lab_notebook_path

DIR_KEYS = ("notebook_dir", "root_dir")


def prepare_url(server: dict, query_str: str = ""):
    """Prepare url to query the jupyter server."""
    token = server["token"]
    if token:
        query_str = f"{query_str}?token={token}"
    url = f"{server['url']}api/sessions{query_str}"

    return url


def query_server(server: dict):
    """Query the jupyter server for sessions' info."""
    # based on https://github.com/msm1089/ipynbname
    try:
        url = prepare_url(server)
        with request.urlopen(url) as req:
            return orjson.loads(req.read())
    except Exception:
        CONN_ERROR = (
            "Unable to access server;\n"
            "querying requires either no security or token based security."
        )
        raise Exception(CONN_ERROR) from None


def running_servers():
    """Return the info about running jupyter servers."""
    nbapp_import = False

    try:
        from notebook.notebookapp import list_running_servers

        nbapp_import = True
        servers_nbapp = list_running_servers()
    except ModuleNotFoundError:
        servers_nbapp = []

    try:
        from jupyter_server.serverapp import list_running_servers

        servers_juserv = list_running_servers()
    except ModuleNotFoundError:
        servers_juserv = []

        if not nbapp_import:
            logger.warning(
                "It looks like you are running jupyter lab "
                "but don't have jupyter-server module installed. "
                "Please install it via pip install jupyter-server"
            )

    return servers_nbapp, servers_juserv


def find_nb_path_via_parent_process():
    """Tries to find the notebook path by inspecting the parent process's command line.

    Requires the 'psutil' library. Heuristic and potentially fragile.
    """
    import psutil

    try:
        current_process = psutil.Process(os.getpid())
        parent_process = current_process.parent()

        if parent_process is None:
            logger.warning("psutil: Could not get parent process.")
            return None

        # Get parent command line arguments
        cmdline = parent_process.cmdline()
        if not cmdline:
            logger.warning(
                f"psutil: Parent process ({parent_process.pid}) has empty cmdline."
            )
            # Maybe check grandparent? This gets complicated quickly.
            return None

        logger.info(f"psutil: Parent cmdline: {cmdline}")

        # Heuristic parsing: Look for 'nbconvert' and '.ipynb'
        # This is fragile and depends on how nbconvert was invoked.
        is_nbconvert_call = False
        potential_path = None

        for i, arg in enumerate(cmdline):
            # Check if 'nbconvert' command is present
            if "nbconvert" in arg.lower():
                # Check if it's the main command (e.g. /path/to/jupyter-nbconvert)
                # or a subcommand (e.g. ['jupyter', 'nbconvert', ...])
                # or a module call (e.g. ['python', '-m', 'nbconvert', ...])
                base_arg = os.path.basename(arg).lower()  # noqa: PTH119
                if (
                    "jupyter-nbconvert" in base_arg
                    or arg == "nbconvert"
                    or (
                        cmdline[i - 1].endswith("python")
                        and arg == "-m"
                        and cmdline[i + 1] == "nbconvert"
                    )
                ):
                    is_nbconvert_call = True

            # Find the argument ending in .ipynb AFTER 'nbconvert' is likely found
            # Or just find the last argument ending in .ipynb as a guess
            if arg.endswith(".ipynb"):
                potential_path = arg  # Store the last one found

        if is_nbconvert_call and "--inplace" not in cmdline:
            raise ValueError(
                "Please execute notebook 'nbconvert' by passing option '--inplace'."
            )

        if is_nbconvert_call and potential_path:
            # We found something that looks like an nbconvert call and an ipynb file
            # The path might be relative to the parent process's CWD.
            # Try to resolve it. Parent CWD might not be notebook dir if called like
            # jupyter nbconvert --execute /abs/path/to/notebook.ipynb
            try:
                # Get parent's CWD
                parent_cwd = parent_process.cwd()
                resolved_path = Path(parent_cwd) / Path(potential_path)
                if resolved_path.is_file():
                    logger.info(f"psutil: Found potential path: {resolved_path}")
                    return resolved_path.resolve()  # Return absolute path
                else:
                    # Maybe the path was already absolute?
                    abs_path = Path(potential_path)
                    if abs_path.is_absolute() and abs_path.is_file():
                        logger.info(
                            f"psutil: Found potential absolute path: {abs_path}"
                        )
                        return abs_path.resolve()
                    else:
                        logger.warning(
                            f"psutil: Potential path '{potential_path}' not found relative to parent CWD '{parent_cwd}' or as absolute path."
                        )
                        return None

            except psutil.AccessDenied:
                logger.warning("psutil: Access denied when getting parent CWD.")
                # Fallback: assume path might be relative to kernel's CWD (less likely)
                maybe_path = Path(potential_path)
                if maybe_path.is_file():
                    return maybe_path.resolve()
                return None  # Give up trying to resolve relative path
            except Exception as e:
                logger.warning(f"psutil: Error resolving path '{potential_path}': {e}")
                return None

        logger.warning(
            "psutil: Could not reliably identify notebook path from parent cmdline."
        )
        return None

    except ImportError:
        logger.warning("psutil library not found. Cannot inspect parent process.")
        return None
    except psutil.Error as e:
        logger.warning(f"psutil error: {e}")
        return None
    except ValueError as ve:  # Explicitly catch and re-raise the intended error
        raise ve
    except Exception as e:
        logger.warning(f"Unexpected error during psutil check: {e}")
        return None


def notebook_path(return_env=False):
    """Return the path to the current notebook.

    Args:
        return_env: If `True`, return the environment of execution:
            `'lab'` for jupyter lab and `'notebook'` for jupyter notebook.
    """
    env = None
    if "NBPRJ_TEST_NBENV" in os.environ:
        env = os.environ["NBPRJ_TEST_NBENV"]

    if "NBPRJ_TEST_NBPATH" in os.environ:
        nb_path = os.environ["NBPRJ_TEST_NBPATH"]
        if return_env:
            return nb_path, "test" if env is None else env
        else:
            return nb_path

    try:
        from IPython import get_ipython
    except ModuleNotFoundError:
        logger.warning("Can not import get_ipython.")
        return None

    # vs code specific
    if "__main__" in sys.modules:
        main_module = sys.modules["__main__"]
        if hasattr(main_module, "__vsc_ipynb_file__"):
            nb_path = main_module.__vsc_ipynb_file__
            return (
                (nb_path, "vs_code" if env is None else env) if return_env else nb_path
            )

    ipython_instance = get_ipython()

    # not in an ipython kernel
    if ipython_instance is None:
        logger.warning("The IPython instance is empty.")
        return None

    config = ipython_instance.config
    # not in a jupyter notebook
    if "IPKernelApp" not in config:
        logger.warning("IPKernelApp is not in ipython_instance.config.")
        return None

    kernel_id = (
        config["IPKernelApp"]["connection_file"].partition("-")[2].split(".", -1)[0]
    )

    servers_nbapp, servers_juserv = running_servers()

    server_exception = None

    for server in chain(servers_nbapp, servers_juserv):
        try:
            session = query_server(server)
        except Exception as e:
            server_exception = e
            continue

        for notebook in session:
            if "kernel" not in notebook or "notebook" not in notebook:
                continue
            if notebook["kernel"].get("id", None) == kernel_id:
                for dir_key in DIR_KEYS:
                    if dir_key in server:
                        nb_path = (
                            PurePath(server[dir_key]) / notebook["notebook"]["path"]
                        )

                        if return_env:
                            if env is None:
                                rt_env = "lab" if dir_key == "root_dir" else "notebook"
                            else:
                                rt_env = env
                            return nb_path, rt_env
                        else:
                            return nb_path

    # trying to get the path through ipylab
    nb_path = _lab_notebook_path()
    if nb_path is not None:
        return (nb_path, "lab" if env is None else env) if return_env else nb_path

    # for newer versions of lab, less safe as it stays the same after file rename
    if "JPY_SESSION_NAME" in os.environ:
        nb_path = PurePath(os.environ["JPY_SESSION_NAME"])
        return (nb_path, "lab" if env is None else env) if return_env else nb_path

    # try inspecting parent process using psutil, needed if notebook is run via nbconvert
    nb_path_psutil = find_nb_path_via_parent_process()
    if nb_path_psutil is not None:
        logger.info("Detected path via psutil parent process inspection.")
        return (
            (nb_path_psutil, "nbconvert" if env is None else env)
            if return_env
            else nb_path_psutil
        )

    # no running servers
    if servers_nbapp == [] and servers_juserv == []:
        logger.warning("Can not find any servers running.")

    logger.warning(
        "Can not find the notebook in any server session or by using other methods."
    )
    if not _ipylab_is_installed():
        logger.warning(
            "Consider installing ipylab (pip install ipylab) if you use jupyter lab."
        )

    if server_exception is not None:
        raise server_exception

    return None

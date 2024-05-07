from pathlib import Path
from time import sleep

from nbproject._is_run_from_ipython import is_run_from_ipython

app = None


# called in __init__.py
def _init_frontend():
    try:
        from ipylab import JupyterFrontEnd

        global app
        if app is None and is_run_from_ipython:
            app = JupyterFrontEnd()
    except ImportError:
        pass


def _save_notebook():
    if app is not None:
        app.commands.execute("docmanager:save")
        sleep(1)


def _reload_notebook():
    if app is not None:
        app.commands.execute("docmanager:reload")


def _lab_notebook_path():
    if app is None:
        return None

    current_session = app.sessions.current_session

    if "name" in current_session:
        nb_path = Path.cwd() / app.sessions.current_session["name"]
    else:
        nb_path = None

    return nb_path


def _ipylab_is_installed():
    if app is not None:
        return True
    try:
        import ipylab

        return True
    except ImportError:
        return False

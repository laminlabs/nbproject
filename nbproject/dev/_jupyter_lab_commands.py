from pathlib import Path
from time import sleep

from ipylab import JupyterFrontEnd

app = None


def _init_frontend():
    global app
    if app is None:
        app = JupyterFrontEnd()


def _save_notebook():
    _init_frontend()

    app.commands.execute("docmanager:save")
    sleep(1)


def _reload_notebook():
    _init_frontend()

    app.commands.execute("docmanager:reload")


def _lab_notebook_path():
    _init_frontend()

    current_session = app.sessions.current_session

    if "name" in current_session:
        nb_path = Path.cwd() / app.sessions.current_session["name"]
    else:
        nb_path = None

    return nb_path

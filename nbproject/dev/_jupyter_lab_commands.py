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

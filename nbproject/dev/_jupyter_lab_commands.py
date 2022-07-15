from time import sleep

from ipylab import JupyterFrontEnd

app = None


def _save_notebook():
    global app
    if app is None:
        app = JupyterFrontEnd()

    app.commands.execute("docmanager:save")
    sleep(1)


def _reload_notebook():
    global app
    if app is None:
        app = JupyterFrontEnd()

    app.commands.execute("docmanager:reload")

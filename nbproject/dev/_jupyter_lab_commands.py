from time import sleep

from ipylab import JupyterFrontEnd

_app = None


def _save_notebook():
    global _app
    if _app is None:
        _app = JupyterFrontEnd()

    _app.commands.execute("docmanager:save")
    sleep(1)


def _restart_notebook():
    global _app
    if _app is None:
        _app = JupyterFrontEnd()

    _app.commands.execute("docmanager:reload")
    _app.commands.execute("notebook:restart-and-run-to-selected")

from time import sleep

from ipylab import JupyterFrontEnd

_app = None


def _save_notebook():
    global _app
    if _app is None:
        _app = JupyterFrontEnd()

    _app.commands.execute("docmanager:save")
    sleep(1)


def _reload_shutdown():
    global _app
    if _app is None:
        _app = JupyterFrontEnd()

    _app.commands.execute("docmanager:reload")  # reload notebook from disk
    # the following line would be desirable but pops up another dialogue,
    # which is confusing
    # _app.commands.execute("docmanager:save")  # orjson writes non-diffable json
    _app.commands.execute("kernelmenu:shutdown")


def _reload_and_restart_notebook():
    global _app
    if _app is None:
        _app = JupyterFrontEnd()

    _app.commands.execute("docmanager:reload")  # reload notebook from disk
    _app.commands.execute("kernelmenu:restart")

    # the below was useful for init, but is not viable for publish()
    # _app.commands.execute("notebook:restart-and-run-to-selected")
    # It'd be nice to execute more cells here, but that's impossible
    # as the kernel is dead at this point
    #
    # "notebook:restart-run-all" is also no alternative, as that will run
    # the entire notebook, which might be undesirable
    # also in combination with something like the below in `Header()` seems hacky
    # as it prints a big "Keyboard Interrupt"
    # if (
    #     time_run - datetime.fromisoformat(nb.metadata["nbproject"]["time_init"])
    # ) < 2:
    # from ipylab import JupyterFrontEnd
    # app = JupyterFrontEnd()
    # app.commands.execute('notebook:interrupt-kernel')

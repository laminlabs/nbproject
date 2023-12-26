from time import sleep

from nbproject._logger import logger


def _save_notebook():
    try:
        from IPython.display import Javascript, display_javascript
    except ModuleNotFoundError:
        logger.warning("Can not import from IPython.")
        return None

    js = Javascript("IPython.notebook.save_notebook()")
    display_javascript(js)

    sleep(1)


def _reload_notebook():
    try:
        from IPython.display import Javascript, display_javascript
    except ModuleNotFoundError:
        logger.warning("Can not import from IPython.")
        return None

    js = Javascript("IPython.notebook.load_notebook(IPython.notebook.notebook_path)")
    display_javascript(js)

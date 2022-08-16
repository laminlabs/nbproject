from time import sleep


def _save_notebook():
    from IPython.display import Javascript, display

    js = Javascript("IPython.notebook.save_notebook()")
    display(js)

    sleep(1)


def _reload_notebook():
    from IPython.display import Javascript, display

    js = Javascript("IPython.notebook.load_notebook(IPython.notebook.notebook_path)")
    display(js)

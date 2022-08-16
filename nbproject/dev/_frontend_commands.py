from . import _classic_nb_commands as _clsnbk
from . import _jupyter_lab_commands as _juplab


def _save_notebook(env):
    if env == "lab":
        _juplab._save_notebook()
    elif env == "notebook":
        _clsnbk._save_notebook()
    else:
        raise ValueError(f"Unrecognized environment {env}.")


def _reload_notebook(env):
    if env == "lab":
        _juplab._reload_notebook()
    elif env == "notebook":
        _clsnbk._reload_notebook()
    else:
        raise ValueError(f"Unrecognized environment {env}.")

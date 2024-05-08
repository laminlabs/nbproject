from typing import Optional, Union

from ._logger import colors, logger
from ._meta import meta
from .dev._check_last_cell import check_last_cell
from .dev._consecutiveness import check_consecutiveness
from .dev._frontend_commands import _save_notebook
from .dev._jupyter_lab_commands import _ipylab_is_installed
from .dev._notebook import read_notebook
from .dev._set_version import set_version


def run_checks_for_publish(
    *, calling_statement: str, i_confirm_i_saved: bool = False, **kwargs
):
    """Runs all checks for publishing."""
    if meta.env == "notebook" or (meta.env == "lab" and _ipylab_is_installed()):
        _save_notebook(meta.env)
    else:
        pretend_no_test_env = (
            kwargs["pretend_no_test_env"] if "pretend_no_test_env" in kwargs else False
        )
        if (
            meta.env == "test" and not pretend_no_test_env
        ):  # do not raise error in test environment
            pass
        elif not i_confirm_i_saved:
            raise RuntimeError(
                "Make sure you save the notebook in your editor before publishing!\n"
                "You can avoid the need for manually saving in Jupyter Lab with ipylab installed"
                " or Notebook, which auto-save the buffer during publish."
            )

    notebook_title = meta.live.title
    title_error = (
        f"No title! Update & {colors.bold('save')} your notebook with a title '# My"
        " title' in the first cell."
    )

    if notebook_title is None:
        logger.error(title_error)
        return "no-title"

    nb = read_notebook(meta._filepath)  # type: ignore
    if not check_last_cell(nb, calling_statement):
        raise RuntimeError("Can only publish from the last code cell of the notebook.")

    if not check_consecutiveness(nb):
        if "proceed_consecutiveness" in kwargs:
            decide = kwargs["proceed_consecutiveness"]
        elif meta.env == "test":
            decide = "y"
        else:
            decide = input("   Do you still want to proceed with publishing? (y/n) ")
        if decide != "y":
            logger.warning("Aborted!")
            return "aborted"

    return "checks-passed"


def finalize_publish(*, calling_statement: str, version: Optional[str] = None):
    meta.store.version = set_version(version)
    meta.store.pypackage = meta.live.pypackage
    meta.store.user_handle = meta.live.user_handle
    meta.store.user_id = meta.live.user_id
    meta.store.user_name = meta.live.user_name
    logger.info(
        f"Set notebook version to {colors.bold(meta.store.version)} & wrote pypackages."
    )
    meta.store.write(calling_statement=calling_statement)
    return None


def publish(
    *,
    version: Optional[str] = None,
    i_confirm_i_saved: bool = False,
    **kwargs,
) -> Union[None, str]:
    """Publish the notebook.

    Runs these checks:
    1. Checks consecutiveness, i.e., whether notebook cells were executed consecutively.
    2. Checks that the notebook has a title.
    3. Checks that the notebook is published from its last cell.

    Writes these data:
    1. Sets version.
    2. Stores currently imported python packages with their versions.

    Returns `None` upon success and an error code otherwise.

    Args:
        version: If `None`, leaves the version at its current value. Otherwise
            sets the version to the passed version. Consider semantic versioning.
        i_confirm_i_saved: Only relevant outside Jupyter Lab as a safeguard against
            losing the editor buffer content because of accidentally publishing.
        kwargs: Additional arguments for publishing.
    """
    if "calling_statement" in kwargs:
        calling_statement = kwargs.pop("calling_statement")
    else:
        calling_statement = "publish("
    result = run_checks_for_publish(
        i_confirm_i_saved=i_confirm_i_saved,
        calling_statement=calling_statement,
        **kwargs,
    )
    if result == "checks-passed":
        return finalize_publish(version=version, calling_statement=calling_statement)
    else:
        return result

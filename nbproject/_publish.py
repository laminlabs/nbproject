from typing import Optional, Union

from ._logger import colors, logger
from ._meta import meta
from .dev._check_last_cell import check_last_cell
from .dev._consecutiveness import check_consecutiveness
from .dev._jupyter_lab_commands import _save_notebook
from .dev._notebook import read_notebook
from .dev._set_version import set_version


def publish(
    *,
    version: Optional[str] = None,
    i_confirm_i_saved: bool = False,
    **kwargs,
) -> Union[None, str]:
    """Publish your notebook before sharing it.

    1. Sets version.
    2. Stores pypackages.
    3. Checks consecutiveness, i.e., whether notebook cells were executed consecutively.
    4. Checks that the notebook has a title.

    This function has to be called in the last code cell of the notebook.

    Returns `None` upon success and an error code otherwise.

    Args:
        version: If `None`, bumps the version from "draft" to "1", from "1" to "2", etc.
            Otherwise sets the version to the passed version.
        i_confirm_i_saved: Only relevant outside Jupyter Lab as a safeguard against
            losing the editor buffer content because of accidentally publishing.
    """
    if "calling_statement" in kwargs:
        calling_statement = kwargs["calling_statement"]
    else:
        calling_statement = "publish("

    notebook_title = meta.live.title
    title_error = (
        f"No title! Update & {colors.bold('save')} your notebook with a title '# My"
        " title' in the first cell."
    )

    if notebook_title is None:
        logger.error(title_error)
        return "no-title"

    if meta._env == "lab":
        _save_notebook()
    else:
        pretend_no_test_env = (
            kwargs["pretend_no_test_env"] if "pretend_no_test_env" in kwargs else False
        )
        if (
            meta._env == "test" and not pretend_no_test_env
        ):  # do not raise error in test environment
            pass
        elif not i_confirm_i_saved:
            raise RuntimeError(
                "Make sure you save the notebook in your editor before publishing!\n"
                "You can avoid the need for manually saving in Jupyter Lab, which auto-saves the buffer during publish."  # noqa
            )

    nb = read_notebook(meta._filepath)  # type: ignore
    if not check_last_cell(nb, calling_statement):
        raise RuntimeError("Can only publish from the last code cell of the notebook.")

    if not check_consecutiveness(nb):
        if meta._env == "test":
            decide = "y"
        else:
            decide = input("   Do you still want to proceed with publishing? (y/n) ")

        if decide != "y":
            logger.warning("Aborted!")
            return "aborted"

    meta.store.version = set_version(version)
    meta.store.pypackage = meta.live.pypackage
    logger.info(
        f"Set notebook version to {colors.bold(meta.store.version)} & wrote pypackages."
    )

    meta.store.write(calling_statement=calling_statement)
    return None

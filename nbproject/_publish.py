from typing import Optional

from ._logger import colors, logger
from ._meta import meta
from .dev._check_last_cell import check_last_cell
from .dev._consecutiveness import check_consecutiveness
from .dev._jupyter_lab_commands import _save_notebook
from .dev._notebook import read_notebook


def publish(
    *,
    version: Optional[str] = None,
    i_confirm_i_saved: bool = False,
    **kwargs,
) -> None:
    """Publish your notebook before sharing it.

    1. Sets a version > "draft".
    2. Stores pypackages.
    3. Checks consecutiveness, i.e., whether notebook cells were executed consecutively.
    4. Checks that the notebook has a title.

    This function has to be called in the last code cell of the notebook.

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

    notebook_title = meta.live.title  # type: ignore
    title_error = (
        "Error: No title! Please update & save your notebook so that it has a"
        " markdown cell with the title: # My title"
    )

    if notebook_title is None:
        raise RuntimeError(title_error)

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

    consecutiveness = check_consecutiveness(nb)

    if not consecutiveness:
        if meta._env == "test":
            decide = "y"
        else:
            decide = input(
                "   The cells in the notebook were not run consecutively, do you want"
                " to proceed with publishing? (y/n) "
            )

        if decide == "n":
            return
        elif decide != "y":
            raise ValueError(
                "Unrecognized input, please use n to abort publishing or y to proceed."
            )

    if version is not None:
        meta.store.version = version  # type: ignore
    else:
        try:
            if meta.store.version == "draft":  # type: ignore
                version = "1"
            else:
                version = str(
                    int(meta.store.version) + 1  # type: ignore
                )  # bump version by 1
            meta.store.version = version  # type: ignore
        except ValueError:
            raise ValueError(
                "The nbproject version cannot be cast to integer. Please pass a version"
                " string."
            )

    meta.store.pypackage = meta.live.pypackage  # type: ignore
    logger.info(
        f"Bumped notebook version to {colors.bold(version)} & wrote pypackages."
    )

    meta.store.write(calling_statement=calling_statement)  # type: ignore

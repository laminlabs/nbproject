from pathlib import Path
from typing import List, Mapping, Optional, Union

from pydantic import BaseModel, Extra

from .._logger import logger
from ._dependency import infer_dependencies_from_file
from ._jupyter_lab_commands import _reload_notebook, _save_notebook
from ._metadata_display import table_metadata
from ._notebook import Notebook, read_notebook, write_notebook


def _change_display_table(metadata: Mapping, notebook: Notebook):
    cells = notebook.cells

    table_html = table_metadata(metadata, notebook)

    for cell in cells:
        if cell["cell_type"] == "code":
            for out in cell["outputs"]:
                if "data" in out and "text/html" in out["data"]:
                    html = out["data"]["text/html"][0]
                    if "<b>version</b>" in html:
                        out["data"]["text/html"][0] = table_html
                        break


def _set_execution_count(calling_statement: str, notebook: Notebook):
    cells = notebook.cells

    prev = 0
    for cell in cells:
        if cell["cell_type"] != "code" or cell["source"] == []:
            continue

        if calling_statement in "".join(cell["source"]):
            cell["execution_count"] = prev + 1

        ccount = cell["execution_count"]
        if ccount is not None:
            prev = ccount


class MetaContainer(BaseModel):
    """The metadata stored in the notebook file."""

    id: str
    """A universal 8-digit base62 ID."""
    time_init: str
    """Time of nbproject init in UTC. Often coincides with notebook creation."""
    dependency: Optional[Mapping[str, str]] = None
    """Dictionary of notebook dependencies and their versions."""
    version: str = "draft"
    """Published version of notebook."""

    class Config:  # noqa
        extra = Extra.allow


class MetaStore:
    """The wrapper class for metadata stored in the notebook file."""

    def __init__(
        self,
        meta_container: MetaContainer,
        filepath: Union[str, Path, None] = None,
        env: Optional[str] = None,
    ):
        self._filepath = filepath
        self._env = env

        self._meta_container = meta_container

    def __getattr__(self, attr_name):
        return getattr(self._meta_container, attr_name)

    def __setattr__(self, attr_name, value):
        if attr_name[0] != "_":
            setattr(self._meta_container, attr_name, value)
        else:
            self.__dict__[attr_name] = value

    def add_dependencies(self, deps: List[str]):
        """Manually add dependencies without versions."""
        if self._meta_container.dependency is None:
            self._meta_container.dependency = {}

        deps_dict = self._meta_container.dependency

        for dep in deps:
            if dep not in deps_dict:
                deps_dict[dep] = ""  # type: ignore

    def update_dependencies(self):
        """Update dependencies in store with live dependencies."""
        if self._meta_container.dependency is None:
            self._meta_container.dependency = {}

        deps_dict = self._meta_container.dependency
        deps = infer_dependencies_from_file(self._filepath)
        deps_dict.update(deps)

    def write(self, **kwargs):
        """Write to file.

        You can edit the nbproject metadata of the current notebook
        by changing `.store` fields and then using this function
        to write the changes to the file.

        Outside Jupyter Lab: Save the notebook before writing.
        """
        if self._env == "lab":
            _save_notebook()

        nb = read_notebook(self._filepath)

        upd_metadata = self._meta_container.dict()
        nb.metadata["nbproject"] = upd_metadata

        _change_display_table(upd_metadata, nb)

        if "calling_statement" in kwargs:
            _set_execution_count(kwargs["calling_statement"], nb)

        write_notebook(nb, self._filepath)

        if self._env == "lab":
            _reload_notebook()
        elif self._env != "test":
            logger.info(
                "File changed on disk! Reload the notebook if you want to continue."
            )
            # sys.exit(0)  # makes CI fail, need to think of a decent way of exiting

    def __repr__(self):
        return f"Wrapper object for the stored metadata:\n  {self._meta_container}"

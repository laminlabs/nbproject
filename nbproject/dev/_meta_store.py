import re
from typing import List, Mapping, Optional, Union

from pydantic import BaseModel, Extra

from .._logger import logger
from ._dependency import infer_dependencies_from_file
from ._jupyter_lab_commands import _reload_shutdown, _restart_notebook, _save_notebook
from ._notebook import read_notebook, write_notebook


def _change_display_version(cells: list, version):
    for cell in cells:
        if cell["cell_type"] == "code":
            for out in cell["outputs"]:
                if "data" in out and "text/html" in out["data"]:
                    html = out["data"]["text/html"][0]
                    if "<b>version</b>" in html:
                        pattern = r"(.+version.+?<td.+?>).+?(</td>.+)"
                        html = re.sub(pattern, rf"\1!!!!{version}\2", html)
                        html = html.replace("!!!!", "")
                        out["data"]["text/html"][0] = html
                        break


class MetaStore(BaseModel):
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

    @property
    def _filepath(self):
        from .._header import _filepath

        return _filepath

    @property
    def _env(self):
        from .._header import _env

        return _env

    def add_dependencies(self, deps: Union[List[str], Mapping[str, str]]):
        """Manually add dependencies."""
        if self.dependency is None:
            self.dependency = {}

        deps_dict = self.dependency

        if isinstance(deps, dict):
            deps_dict.update(deps)  # type: ignore
        elif isinstance(deps, list):
            for dep in deps:
                deps_dict[dep] = ""  # type: ignore

    def update_dependencies(self):
        """Update dependencies in store with live dependencies."""
        if self.dependency is None:
            self.dependency = {}

        deps = infer_dependencies_from_file(self._filepath)

        deps_dict = self.dependency

        if isinstance(deps, dict):
            deps_dict.update(deps)  # type: ignore
        elif isinstance(deps, list):
            for dep in deps:
                deps_dict[dep] = ""  # type: ignore

    def write(self, restart=True):
        """Write to file and shutdown notebook kernel.

        You can edit the nbproject metadata of the current notebook
        by changing `.store` fields and then using this function
        to write the changes to the file. Save the notebook before writing.
        """
        if self._env == "lab":
            _save_notebook()

        nb = read_notebook(self._filepath)
        nb.metadata["nbproject"] = self.dict()
        # also update displayed version number
        # this is ugly right now but important
        _change_display_version(nb.cells, self.version)

        write_notebook(nb, self._filepath)

        if self._env == "lab":
            if restart:
                _restart_notebook()
            else:
                logger.info("Reload notebook from disk & shutdown kernel.")
                _reload_shutdown()
        elif self._env != "test":
            logger.info(
                "File changed on disk! Reload and restart the"
                " notebook if you want to continue."
            )
            # sys.exit(0)  # makes CI fail, need to think of a decent way of exiting

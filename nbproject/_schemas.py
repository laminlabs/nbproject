import nbformat as nbf
from pathlib import Path
from datetime import datetime, timezone
from ._header import nbproject_uid
from ._utils import public_vars


class NBRecord:
    def __init__(self, nb: nbf.NotebookNode):
        self._nb = nb

        metadata = nb.metadata
        if "nbproject" in metadata:
            self._filled = True
            for key, value in metadata["nbproject"].items():
                setattr(self, "_" + key, value)
        else:
            self._filled = False

    @property
    def uid(self):
        if not hasattr(self, "_uid"):
            self._filled = False
            self._uid = nbproject_uid()
        return self._uid

    @property
    def time_init(self):
        if not hasattr(self, "_time_init"):
            self._filled = False
            self._time_init = datetime.now(timezone.utc).isoformat()
        return self._time_init

    def write(self, nb_path: Path, overwrite: bool):
        nbproj_data = nbf.NotebookNode(public_vars(self))
        if overwrite or not self._filled:
            self._nb.metadata["nbproject"] = nbproj_data
            nbf.write(self._nb, nb_path)
            self._filled = True


class YAMLRecord:
    # this is for ordering
    _take_keys = ("time_init", "name", "location")

    def __init__(self, nb_path: Path, nb_record: NBRecord):
        # load fields from the notebooks' metadata
        nb_record_fields = public_vars(nb_record)

        self._uid = nb_record_fields.pop("uid")

        for key, value in nb_record_fields.items():
            setattr(self, key, value)

        # here set fields specific to yaml
        self.time_init = datetime.fromisoformat(self.time_init)
        self.time_init = self.time_init.strftime("%Y-%m-%d %H:%M")

        self.location = nb_path.parent.as_posix()
        self.name = nb_path.name

    def put(self, yaml_project: dict):
        if self._uid not in yaml_project:
            yaml_project[self._uid] = {}

        yaml_record = yaml_project[self._uid]
        fields = public_vars(self)
        for key in self._take_keys:
            yaml_record[key] = fields.pop(key)
        yaml_record.update(fields)

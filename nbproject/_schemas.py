from datetime import datetime, timezone
from pathlib import Path

from ._utils import public_fields
from .dev._initialize import nbproject_id
from .dev._notebook import Notebook, write_notebook


class NBRecord:
    def __init__(self, nb: Notebook):
        self._nb = nb

        metadata = nb.metadata
        if "nbproject" in metadata:
            self._filled = True
            for key, value in metadata["nbproject"].items():
                setattr(self, "_" + key, value)
        else:
            self._filled = False

    def check_attr(self, attr):
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            self._filled = False
            return None

    def __setattr__(self, attr_name, value):
        if attr_name[0] != "_":
            present_value = self.check_attr(attr_name)
            if present_value != value:
                self.__dict__[attr_name] = value
                self._filled = False
        else:
            self.__dict__[attr_name] = value

    @property
    def id(self):
        id = self.check_attr("_id")
        if id is None:
            id = nbproject_id()
            self._id = id
        return id

    @property
    def time_init(self):
        time_init = self.check_attr("_time_init")
        if time_init is None:
            time_init = datetime.now(timezone.utc).isoformat()
            self._time_init = time_init
        return time_init

    @property
    def version(self):
        version = self.check_attr("_version")
        if version is None:
            version = "draft"
            self._version = "draft"
        return version

    @property
    def pypackage(self):
        if "pypackage" in self.__dict__:
            return self.__dict__["pypackage"]
        elif hasattr(self, "_pypackage"):
            return self._pypackage
        else:
            return None

    def write(self, nb_path: Path, overwrite: bool):
        nbproj_data = public_fields(self)
        if overwrite or not self._filled:
            self._nb.metadata["nbproject"] = nbproj_data
            write_notebook(self._nb, nb_path)
            self._filled = True


class YAMLRecord:
    # this is for ordering and also ignore this when reading yaml fields
    _take_keys = ("time_init", "name", "version", "location")

    def __init__(self, nb_path: Path, nb_record: NBRecord, yaml_proj: dict):
        self._yaml_proj = yaml_proj
        self._nb_record = nb_record
        # load fields from the notebooks' metadata
        nb_record_fields = public_fields(nb_record)

        self._id = nb_record_fields.pop("id")

        for key, value in nb_record_fields.items():
            setattr(self, key, value)

        # take field from yaml, takes precedence over nb_record
        if self._id in self._yaml_proj:
            for key, value in self._yaml_proj[self._id].items():
                if key not in self._take_keys:
                    setattr(self, key, value)

        # here set fields specific to yaml
        self.time_init = datetime.fromisoformat(self.time_init)  # type: ignore
        self.time_init = self.time_init.strftime("%Y-%m-%d %H:%M")  # type: ignore

        self.location = nb_path.parent.as_posix()
        self.name = nb_path.name

    def put_metadata(self):
        for key, value in public_fields(self).items():
            if key not in self._take_keys:
                setattr(self._nb_record, key, value)

    def put_yaml(self):
        yaml_project = self._yaml_proj

        if self._id not in yaml_project:
            yaml_project[self._id] = {}

        yaml_record = yaml_project[self._id]
        fields = public_fields(self)
        for key in self._take_keys:
            yaml_record[key] = fields.pop(key)
        yaml_record.update(fields)

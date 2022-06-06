import orjson
from pathlib import Path
from datetime import datetime, timezone
from ._header import nbproject_uid
from ._utils import public_fields


class NBRecord:
    def __init__(self, nb: dict):
        self._nb = nb

        metadata = nb["metadata"]
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
    def uid(self):
        uid = self.check_attr("_uid")
        if uid is None:
            uid = nbproject_uid()
            self._uid = uid
        return uid

    @property
    def time_init(self):
        time_init = self.check_attr("_time_init")
        if time_init is None:
            time_init = datetime.now(timezone.utc).isoformat()
            self._time_init = time_init
        return time_init

    @property
    def dependency(self):
        if "dependency" in self.__dict__:
            return self.__dict__["dependency"]
        elif hasattr(self, "_dependency"):
            return self._dependency
        else:
            return None

    def write(self, nb_path: Path, overwrite: bool):
        nbproj_data = public_fields(self)
        if overwrite or not self._filled:
            self._nb["metadata"]["nbproject"] = nbproj_data
            with open(nb_path, "wb") as f:
                f.write(orjson.dumps(self._nb))
            self._filled = True


class YAMLRecord:
    # this is for ordering and also ignore this than reading yaml fields
    _take_keys = ("time_init", "name", "location")

    def __init__(self, nb_path: Path, nb_record: NBRecord, yaml_proj: dict):
        self._yaml_proj = yaml_proj
        self._nb_record = nb_record
        # load fields from the notebooks' metadata
        nb_record_fields = public_fields(nb_record)

        self._uid = nb_record_fields.pop("uid")

        for key, value in nb_record_fields.items():
            setattr(self, key, value)

        # take field from yaml, takes precedence over nb_record
        if self._uid in self._yaml_proj:
            for key, value in self._yaml_proj[self._uid].items():
                if key not in self._take_keys:
                    setattr(self, key, value)

        # here set fields specific to yaml
        self.time_init = datetime.fromisoformat(self.time_init)
        self.time_init = self.time_init.strftime("%Y-%m-%d %H:%M")

        self.location = nb_path.parent.as_posix()
        self.name = nb_path.name

    def put_metadata(self):
        for key, value in public_fields(self).items():
            if key not in self._take_keys:
                setattr(self._nb_record, key, value)

    def put_yaml(self):
        yaml_project = self._yaml_proj

        if self._uid not in yaml_project:
            yaml_project[self._uid] = {}

        yaml_record = yaml_project[self._uid]
        fields = public_fields(self)
        for key in self._take_keys:
            yaml_record[key] = fields.pop(key)
        yaml_record.update(fields)

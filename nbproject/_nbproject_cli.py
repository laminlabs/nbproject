import yaml
import nbformat as nbf

from pathlib import Path
from itertools import chain

from ._header import uuid4_hex


class PathRecord:
    def __init__(self, filepath: Path):
        self.name = filepath.name
        self.loc = filepath.parent.as_posix()

    def compare_write(self, record):
        # todo: make extendable
        if "name" not in record or record["name"] != self.name:
            record["name"] = self.name
        if "location" not in record or record["location"] != self.loc:
            record["location"] = self.loc


def find_upwards(cwd: Path, filename: str):
    if cwd == Path(cwd.anchor):
        return None

    fullpath = cwd / filename

    return fullpath if fullpath.exists() else find_upwards(cwd.parent, filename)


def nbs_from_files_dirs(files_dirs):
    nbs = []

    for file_dir in files_dirs:
        file_dir = Path(file_dir)
        if file_dir.is_dir():
            nbs.append(file_dir.glob("**/*.ipynb"))
        else:
            if file_dir.suffix == ".ipynb":
                nbs.append([file_dir])
            else:
                print("The file", file_dir, "is not a notebook, ignoring.")

    return chain(*nbs)


def init():
    cwd = Path.cwd()

    yaml_exists = find_upwards(cwd, "nbproject.yaml")
    if yaml_exists is not None:
        print("You are already in the nbproject (sub)folder.")
        print("Yaml of the project is:", yaml_exists.as_posix())
        return

    nbs = cwd.glob("**/*.ipynb")

    init_yaml = {}

    for nb_path in nbs:
        if ".ipynb_checkpoints/" in nb_path.as_posix():
            continue

        nb_path = nb_path.relative_to(cwd)

        nb_content = nbf.read(nb_path, as_version=nbf.NO_CONVERT)

        if "nbproject_uuid" not in nb_content.metadata:
            nb_uuid = uuid4_hex()
            nb_content.metadata["nbproject_uuid"] = nb_uuid
            nbf.write(nb_content, nb_path)
        else:
            nb_uuid = nb_content.metadata["nbproject_uuid"]

        nb_record = {}
        PathRecord(nb_path).compare_write(nb_record)

        init_yaml[nb_uuid] = nb_record

    new_file = "nbproject.yaml"
    with open(new_file, "w") as stream:
        yaml.dump(init_yaml, stream, sort_keys=False)
    print("Created", cwd / new_file)


def sync(files_dirs, deps=False, versions=False):
    cwd = Path.cwd()

    yaml_file = find_upwards(cwd, "nbproject.yaml")

    if yaml_file is None:
        print("You are not inside an nbproject folder, use init.")
        return
    else:
        print("Yaml of the project is:", yaml_file.as_posix())

    proj_dir = yaml_file.parent

    with open(yaml_file, "r") as stream:
        yaml_proj = yaml.load(stream, Loader=yaml.FullLoader)

    nbs = nbs_from_files_dirs(files_dirs)

    n_nbs = 0

    for nb_path in nbs:
        if ".ipynb_checkpoints/" in nb_path.as_posix():
            continue

        n_nbs += 1

        nb_content = nbf.read(nb_path, as_version=nbf.NO_CONVERT)
        if "nbproject_uuid" not in nb_content.metadata:
            nb_uuid = uuid4_hex()
            nb_content.metadata["nbproject_uuid"] = nb_uuid
            nbf.write(nb_content, nb_path)
        else:
            nb_uuid = nb_content.metadata["nbproject_uuid"]

        if nb_uuid not in yaml_proj:
            yaml_proj[nb_uuid] = {}
            nb_record = yaml_proj[nb_uuid]
        else:
            nb_record = yaml_proj[nb_uuid]

        nb_path = nb_path.resolve().relative_to(proj_dir)
        PathRecord(nb_path).compare_write(nb_record)

        if deps:
            from ._dependencies import get_deps_nb

            deps = get_deps_nb(nb_content, versions=versions)
            nb_record["dependencies"] = deps

    with open(yaml_file, "w") as stream:
        yaml.dump(yaml_proj, stream, sort_keys=False)
    print("Synced", n_nbs, "notebooks.")

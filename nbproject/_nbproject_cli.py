import yaml
import nbformat as nbf

from pathlib import Path
from itertools import chain
from datetime import datetime, timezone

from ._header import uuid4_hex
from ._logger import logger

from typing import Iterator


# todo: replace with configurable schema
class ProjSchema:
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


def nbs_from_files_dirs(files_dirs: Iterator[str]):
    nbs = []

    for file_dir in files_dirs:
        file_dir = Path(file_dir)
        if file_dir.is_dir():
            nbs.append(file_dir.glob("**/*.ipynb"))
        else:
            if file_dir.suffix == ".ipynb":
                nbs.append([file_dir])
            else:
                logger.info(f"The file {file_dir} is not a notebook, ignoring.")

    return chain(*nbs)


def init():
    cwd = Path.cwd()

    yaml_exists = find_upwards(cwd, "nbproject.yml")
    if yaml_exists is not None:
        logger.info("You are already in the nbproject (sub)folder.")
        logger.info(f"Yaml of the project is: {yaml_exists.as_posix()}.")
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
            nb_time_init = datetime.now(timezone.utc).isoformat()

            nb_content.metadata["nbproject_uuid"] = nb_uuid
            nb_content.metadata["nbproject_time_init"] = nb_time_init
            nbf.write(nb_content, nb_path)
        else:
            nb_uuid = nb_content.metadata["nbproject_uuid"]
            nb_time_init = nb_content.metadata["nbproject_time_init"]

        nb_record = {}
        nb_record["time_init"] = nb_time_init
        ProjSchema(nb_path).compare_write(nb_record)

        init_yaml[nb_uuid] = nb_record

    new_file = "nbproject.yml"
    with open(new_file, "w") as stream:
        yaml.dump(init_yaml, stream, sort_keys=False)
    logger.info(f"Created {cwd / new_file}.")


def sync(
    files_dirs: Iterator[str], parse_deps: bool = False, pin_versions: bool = False
):
    cwd = Path.cwd()

    yaml_file = find_upwards(cwd, "nbproject.yml")

    if yaml_file is None:
        logger.info("You are not inside an nbproject folder, use init.")
        return
    else:
        logger.info(f"Yaml of the project is: {yaml_file.as_posix()}.")

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
            nb_time_init = datetime.now(timezone.utc).isoformat()

            nb_content.metadata["nbproject_uuid"] = nb_uuid
            nb_content.metadata["nbproject_time_init"] = nb_time_init
        else:
            nb_uuid = nb_content.metadata["nbproject_uuid"]
            nb_time_init = nb_content.metadata["nbproject_time_init"]

        if nb_uuid not in yaml_proj:
            yaml_proj[nb_uuid] = {}
            nb_record = yaml_proj[nb_uuid]
        else:
            nb_record = yaml_proj[nb_uuid]

        nb_record["time_init"] = nb_time_init

        nb_path_format = nb_path.resolve().relative_to(proj_dir)
        ProjSchema(nb_path_format).compare_write(nb_record)

        if parse_deps:
            from ._dependencies import get_deps_nb

            deps = get_deps_nb(nb_content, pin_versions=pin_versions)
            nb_record["dependencies"] = deps

        deps = nb_record.get("dependencies", [])
        deps_field = "nbproject_dependencies"
        if (
            deps_field not in nb_content.metadata
            or nb_content.metadata[deps_field] != deps
        ):
            nb_content.metadata[deps_field] = deps

        nbf.write(nb_content, nb_path)

    with open(yaml_file, "w") as stream:
        yaml.dump(yaml_proj, stream, sort_keys=False)
    logger.info(f"Synced {n_nbs} notebooks.")


def reqs(files_dirs: Iterator[str]):
    # todo: check different versions and do some resolution for conflicting versions
    nbs = nbs_from_files_dirs(files_dirs)

    deps = set()

    for nb_path in nbs:
        if ".ipynb_checkpoints/" in nb_path.as_posix():
            continue

        nb_content = nbf.read(nb_path, as_version=nbf.NO_CONVERT)
        if "nbproject_dependencies" not in nb_content.metadata:
            logger.info(
                "Uninitialized or unsynced notebooks, use > nbproject init or >"
                " nbproject sync ."
            )
            return
        nb_deps = nb_content.metadata["nbproject_dependencies"]
        deps.update(nb_deps)

    requirments = "\n".join(deps)
    with open("requirments.txt", "w") as stream:
        stream.write(requirments)
    logger.info("Created requirments.txt.")

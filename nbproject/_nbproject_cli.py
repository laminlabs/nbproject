# This file contains the functions to process the cli commands.


import yaml
import nbformat as nbf
from pathlib import Path
from itertools import chain
from typing import Iterator
from ._logger import logger
from ._schemas import NBRecord, YAMLRecord


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

    yaml_filled = find_upwards(cwd, "nbproject.yml")
    if yaml_filled is not None:
        logger.info("You are already in the nbproject (sub)folder.")
        logger.info(f"Yaml of the project is: {yaml_filled.as_posix()}.")
        return

    nbs = cwd.glob("**/*.ipynb")

    init_yaml = {}

    for nb_path in nbs:
        if ".ipynb_checkpoints/" in nb_path.as_posix():
            continue

        nb_path = nb_path.relative_to(cwd)

        nb = nbf.read(nb_path, as_version=nbf.NO_CONVERT)

        nbproj_record = NBRecord(nb)
        nbproj_record.write(nb_path, overwrite=False)

        yaml_record = YAMLRecord(nb_path, nbproj_record)
        yaml_record.put(init_yaml)

    new_file = "nbproject.yml"
    with open(new_file, "w") as stream:
        yaml.dump(init_yaml, stream, sort_keys=False)
    logger.info(f"Created {cwd / new_file}.")

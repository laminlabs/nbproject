# This file contains the functions to process the cli commands.
from itertools import chain
from pathlib import Path
from typing import Iterator, Union

import yaml  # type: ignore

from ._logger import logger
from ._schemas import NBRecord, YAMLRecord
from .dev._notebook import read_notebook, write_notebook
from .dev._pypackage import infer_pypackages_from_nb, resolve_versions


def find_upwards(cwd: Path, filename: str):
    if cwd == Path(cwd.anchor):
        return None

    fullpath = cwd / filename

    return fullpath if fullpath.exists() else find_upwards(cwd.parent, filename)


def notebooks_from_files_dirs(files_dirs: Iterator[Union[str, Path]]):
    nbs = []

    for file_dir in files_dirs:
        file_dir = Path(file_dir)
        if file_dir.is_dir():
            nbs.append(file_dir.glob("**/*.ipynb"))
        else:
            if file_dir.suffix == ".ipynb":
                nbs.append([file_dir])  # type: ignore
            else:
                logger.info(f"The file {file_dir} is not a notebook, ignoring.")

    return chain(*nbs)


def init():
    cwd = Path.cwd()

    yaml_filled = find_upwards(cwd, "nbproject_metadata.yml")
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

        nb = read_notebook(nb_path)

        nbproj_record = NBRecord(nb)
        nbproj_record.write(nb_path, overwrite=False)

        yaml_record = YAMLRecord(nb_path, nbproj_record, init_yaml)
        yaml_record.put_yaml()

    new_file = "nbproject_metadata.yml"
    with open(new_file, "w") as stream:
        yaml.dump(init_yaml, stream, sort_keys=False)
    logger.info(f"Created {cwd / new_file}.")


def sync(
    files_dirs: Iterator[str], parse_deps: bool = False, pin_versions: bool = False
):
    cwd = Path.cwd()
    yaml_file = find_upwards(cwd, "nbproject_metadata.yml")

    if yaml_file is None:
        logger.info("You are not inside an nbproject folder, use init.")
        return
    else:
        logger.info(f"Yaml of the project is: {yaml_file.as_posix()}.")

    with open(yaml_file, "r") as stream:
        yaml_proj = yaml.load(stream, Loader=yaml.FullLoader)

    nbs = notebooks_from_files_dirs(files_dirs)
    n_nbs = 0
    for nb_path in nbs:
        if ".ipynb_checkpoints/" in nb_path.as_posix():
            continue
        n_nbs += 1

        nb = read_notebook(nb_path)

        nbproj_record = NBRecord(nb)
        yaml_record = YAMLRecord(nb_path, nbproj_record, yaml_proj)

        if parse_deps:
            deps = infer_pypackages_from_nb(nb, pin_versions=pin_versions)
            yaml_record.pypackage = deps  # type: ignore

        yaml_record.put_metadata()
        yaml_record.put_yaml()

        nbproj_record.write(nb_path, overwrite=False)

    with open(yaml_file, "w") as stream:
        yaml.dump(yaml_proj, stream, sort_keys=False)
    logger.info(f"Synced {n_nbs} notebooks.")


def reqs(files_dirs: Iterator[str]):
    # todo: check different versions and do some resolution for conflicting versions
    gather_deps = []

    nbs = notebooks_from_files_dirs(files_dirs)
    for nb_path in nbs:
        if ".ipynb_checkpoints/" in nb_path.as_posix():
            continue

        nb = read_notebook(nb_path)

        if "nbproject" not in nb.metadata:
            logger.info(
                "Uninitialized or unsynced notebooks, use > nbproject init or >"
                " nbproject sync ."
            )
            return
        nbproj_metadata = nb.metadata["nbproject"]
        if "pypackage" in nbproj_metadata:
            gather_deps.append(nbproj_metadata["pypackage"])

    deps = resolve_versions(gather_deps)
    deps = [pkg + f"=={ver}" if ver != "" else pkg for pkg, ver in deps.items()]

    requirments = "\n".join(deps)
    with open("requirments.txt", "w") as stream:
        stream.write(requirments)

    logger.info("Created `requirements.txt`.")


def publish(files_dirs: Iterator[str]):
    nbs = notebooks_from_files_dirs(files_dirs)
    n_nbs = 0
    for nb_path in nbs:
        if ".ipynb_checkpoints/" in nb_path.as_posix():
            continue

        nb = read_notebook(nb_path)

        if "nbproject" in nb.metadata:
            nbproject_meta = nb.metadata["nbproject"]
            add_pkgs = None
            if "pypackage" in nbproject_meta:
                add_pkgs = nbproject_meta["pypackage"].keys()
            nbproject_meta["pypackage"] = infer_pypackages_from_nb(
                nb, add_pkgs, pin_versions=True
            )

            version = "draft"
            if "version" in nbproject_meta:
                version = nbproject_meta["version"]
            version = "1" if version == "draft" else str(int(version) + 1)
            nbproject_meta["version"] = version

            write_notebook(nb, nb_path)

            n_nbs += 1

        logger.info(f"Pubished {n_nbs} notebooks.")

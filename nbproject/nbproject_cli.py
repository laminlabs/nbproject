import yaml
from glob import iglob
from nbformat import read, write, NO_CONVERT
from pathlib import PurePath

from ._header import uuid4_hex
from ._deps import get_deps_nb

import os

cwd = os.getcwd()
print(cwd)


def init():
    nbs_iter = iglob("./**/*.ipynb", recursive=True)

    init_yaml = {}

    for nb_path in nbs_iter:
        nb_content = read(nb_path, as_version=NO_CONVERT)

        if "nbproject_uuid" not in nb_content.metadata:
            nb_uuid = uuid4_hex()
            nb_content.metadata["nbproject_uuid"] = nb_uuid
            write(nb_content, nb_path)
        else:
            nb_uuid = nb_content.metadata["nbproject_uuid"]

        nb_record = {}
        nb_path = PurePath(nb_path)
        nb_record["name"] = nb_path.name
        nb_record["path"] = nb_path.parent.as_posix()

        init_yaml[nb_uuid] = nb_record

    with open("nbproject.yaml", "w") as stream:
        yaml.dump(init_yaml, stream, sort_keys=False)


def sync(deps=False, versions=False):
    with open("nbproject.yaml", "r") as stream:
        proj_yaml = yaml.load(stream, Loader=yaml.FullLoader)

    nbs_iter = iglob("./**/*.ipynb", recursive=True)

    for nb_path in nbs_iter:
        nb_content = read(nb_path, as_version=NO_CONVERT)
        if "nbproject_uuid" not in nb_content.metadata:
            nb_uuid = uuid4_hex()
            nb_content.metadata["nbproject_uuid"] = nb_uuid
            write(nb_content, nb_path)
        else:
            nb_uuid = nb_content.metadata["nbproject_uuid"]

        nb_path = PurePath(nb_path)
        if nb_uuid not in proj_yaml:
            proj_yaml[nb_uuid] = {}
            nb_record = proj_yaml[nb_uuid]

            nb_record["name"] = nb_path.name
            nb_record["path"] = nb_path.parent.as_posix()
        else:
            nb_record = proj_yaml[nb_uuid]
            if nb_path.name != nb_record["name"]:
                nb_record["name"] = nb_path.name
            if nb_record["path"] != nb_path.parent.as_posix():
                nb_record["path"] = nb_path.parent.as_posix()

        if deps:
            deps = get_deps_nb(nb_content, versions=versions)
            if versions:
                deps_vers = []
                for d, v in zip(*deps):
                    if v == "":
                        deps_vers.append(d)
                    else:
                        deps_vers.append(d + "==" + v)
            else:
                deps_vers = deps
            nb_record["dependencies"] = deps_vers

    with open("nbproject.yaml", "w") as stream:
        yaml.dump(proj_yaml, stream, sort_keys=False)

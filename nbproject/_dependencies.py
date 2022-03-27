from importlib_metadata import packages_distributions, version, PackageNotFoundError
from nbformat import NotebookNode
from ast import parse, walk, Import, ImportFrom
from stdlib_list import stdlib_list

from typing import Union

# todo: maybe infer proper python version for the libs from the notebook metadata
std_libs = set(stdlib_list())
pkgs_dists = packages_distributions()


def cell_imports(cell_source: str):
    # based on the package https://github.com/bndr/pipreqs for python scripts
    tree = parse(cell_source)
    for node in walk(tree):
        if isinstance(node, Import):
            for subnode in node.names:
                name = subnode.name.partition(".")[0]
                if name != "":
                    yield name
        elif isinstance(node, ImportFrom):
            name = node.module.partition(".")[0]
            if name != "":
                yield name


def get_deps_nb(content: Union[NotebookNode, dict, list], versions: bool = False):
    # parse the notebook content and infer all dependencies
    if (
        isinstance(content, NotebookNode) or isinstance(content, dict)
    ) and "cells" in content:
        cells = content["cells"]
    elif isinstance(content, list) and len(content) > 0 and "cell_type" in content[0]:
        cells = content
    else:
        raise ValueError("Invalid content - neither notebook nor cells.")

    pkgs = set()

    for cell in cells:
        if cell["cell_type"] != "code":
            continue

        cell_source = cell["source"]
        if "import" not in cell_source:
            continue
        else:
            for imp in cell_imports(cell_source):
                if imp in std_libs:
                    continue
                if imp in pkgs_dists:
                    pkgs.update(pkgs_dists[imp])
                else:
                    pkgs.add(imp)

    pkgs = list(pkgs)
    if not versions:
        return pkgs

    with_versions = []
    for pkg in pkgs:
        try:
            with_versions.append(pkg + "==" + version(pkg))
        except PackageNotFoundError:
            with_versions.append(pkg)
    return with_versions

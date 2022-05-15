import sys
import re
import packaging
from importlib_metadata import packages_distributions, version, PackageNotFoundError
from nbformat import NotebookNode
from ast import parse, walk, Import, ImportFrom
from typing import Union, List, Literal
from operator import gt, lt


major, minor = sys.version_info[0], sys.version_info[1]
if major == 3 and minor > 9:
    std_libs = sys.stdlib_module_names
else:
    from stdlib_list import stdlib_list

    std_libs = set(stdlib_list(f"{major}.{minor}"))

pkgs_dists = packages_distributions()


def cell_imports(cell_source: str):
    # based on the package https://github.com/bndr/pipreqs for python scripts
    # parses python import statements in the code cells

    # quck hack to ignore jupyter magics
    if "%" in cell_source:
        pattern = "^ *%{1,2}\w+ *"  # noqa: W605
        cell_source = re.split(pattern, cell_source, flags=re.MULTILINE)
        cell_source = "".join(cell_source)

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


def notebook_deps(content: Union[NotebookNode, dict, list], pin_versions: bool = False):
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

    pkgs = {pkg: "" for pkg in pkgs}
    if not pin_versions:
        return pkgs

    for pkg in pkgs:
        try:
            pkg_ver = version(pkg)
        except PackageNotFoundError:
            pkg_ver = ""
        pkgs[pkg] = pkg_ver

    return pkgs


def resolve_versions(
    notebooks_pkgs: List[dict], strategy: Literal["older", "newer"] = "newer"
):
    parse_version = packaging.version.parse

    if strategy == "newer":
        cmp = gt
    elif strategy == "older":
        cmp = lt
    else:
        raise ValueError("Unknown package resolution strategy.")

    def resolve(a, b):
        if a == "":
            return b
        elif b == "":
            return a
        else:
            return a if cmp(parse_version(a), parse_version(b)) else b

    resolved = {}
    for pkgs in notebooks_pkgs:
        for pkg, ver in pkgs.items():
            if pkg not in resolved:
                resolved[pkg] = ver
            else:
                resolved[pkg] = resolve(resolved[pkg], ver)

    return resolved

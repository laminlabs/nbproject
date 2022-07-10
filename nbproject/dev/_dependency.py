import re
import sys
from ast import Import, ImportFrom, parse, walk
from operator import gt, lt
from typing import Iterable, List, Literal, Optional, Union  # noqa

from importlib_metadata import PackageNotFoundError, packages_distributions, version

from ._notebook import Notebook, read_notebook

std_libs = None
pkgs_dists = None


def _load_pkgs_info():
    global std_libs
    global pkgs_dists

    major, minor = sys.version_info[0], sys.version_info[1]
    if major == 3 and minor > 9:
        std_libs = sys.stdlib_module_names  # type: ignore
    else:
        from stdlib_list import stdlib_list

        std_libs = set(stdlib_list(f"{major}.{minor}"))

    pkgs_dists = packages_distributions()


def _get_version(pkg):
    try:
        pkg_ver = version(pkg)
    except PackageNotFoundError:
        pkg_ver = ""
    return pkg_ver


def cell_imports(cell_source: str):
    # based on the package https://github.com/bndr/pipreqs for python scripts
    # parses python import statements in the code cells
    tree = parse(cell_source)
    for node in walk(tree):
        if isinstance(node, Import):
            for subnode in node.names:
                name = subnode.name.partition(".")[0]
                if name != "":
                    yield name
        elif isinstance(node, ImportFrom):
            name = node.module.partition(".")[0]  # type: ignore
            if name != "":
                yield name


def infer_dependencies_from_file(filepath: str):
    """Parse notebook file and infer all dependencies.

    This accounts for additional dependencies in the file metadata.
    """
    nb = read_notebook(filepath)
    add_pkgs = None
    if "nbproject" in nb.metadata and "dependency" in nb.metadata["nbproject"]:
        if nb.metadata["nbproject"]["dependency"] is not None:
            add_pkgs = nb.metadata["nbproject"]["dependency"].keys()
    return infer_dependencies_from_nb(nb, add_pkgs, pin_versions=True)


def infer_dependencies_from_nb(
    content: Union[Notebook, list],
    add_pkgs: Optional[Iterable] = None,
    pin_versions: bool = True,
):
    """Parse notebook object and infer all dependencies.

    Args:
        nb: A notebook or a list of cells to parse for dependencies.
        add_pkgs: Additional packages to add.
        pin_versions: If `True`, fixes versions from the current environment.

    Examples:
        >>> dependencies = nbproject.dev.infer_dependencies(nb)
        >>> dependencies
        {"scanpy": "1.8.7", "pandas": "1.4.3"}
    """
    if isinstance(content, Notebook):
        cells = content.cells
    elif isinstance(content, list) and len(content) > 0 and "cell_type" in content[0]:
        cells = content
    else:
        raise ValueError("Invalid content - neither notebook nor cells.")

    if std_libs is None or pkgs_dists is None:
        _load_pkgs_info()

    pkgs = set()
    magics_re = None

    for cell in cells:
        if cell["cell_type"] != "code":
            continue

        # assuming we read the notebook with a json reader
        cell_source = "".join(cell["source"])
        if "import" not in cell_source:
            continue
        else:
            # quick hack to ignore jupyter magics
            if "%" in cell_source:
                if magics_re is None:
                    magics_re = re.compile(r"^( *)%{1,2}\w+ *", flags=re.MULTILINE)
                cell_source = magics_re.sub(r"\1", cell_source)

            for imp in cell_imports(cell_source):
                if imp in std_libs:  # type: ignore
                    continue
                if imp in pkgs_dists:  # type: ignore
                    pkgs.update(pkgs_dists[imp])  # type: ignore
                else:
                    pkgs.add(imp)

    if add_pkgs is not None:
        pkgs.update(add_pkgs)

    pkgs = {pkg: "" for pkg in pkgs}  # type: ignore
    if not pin_versions:
        return pkgs

    for pkg in pkgs:
        pkgs[pkg] = _get_version(pkg)  # type: ignore

    return pkgs


def resolve_versions(
    notebooks_pkgs: List[dict], strategy: Literal["older", "newer"] = "newer"
):
    """Harmonize packages' versions from lists of packages."""
    import packaging.version

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

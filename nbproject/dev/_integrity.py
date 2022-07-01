from typing import Optional

from loguru import logger

from ._notebook import Notebook


def check_integrity(nb: Notebook, ignore_code: Optional[str] = None) -> list:
    """Get integrity status of the passed notebook.

    Returns those cell transitions that violate execution at increments of 1
    as a list of tuples.

    Args:
        nb: The notebook to check.
        ignore_code: Ignore cells that contain this code.
    """
    cells = nb.cells

    violations = []
    prev = 0

    for cell in cells:
        if cell["cell_type"] != "code" or cell["source"] == []:
            continue

        if ignore_code is not None and ignore_code in "".join(cell["source"]):
            continue

        ccount = cell["execution_count"]
        if ccount is None or ccount - prev != 1:
            violations.append((prev, ccount))

        prev = ccount

    # ignore the very last code cell of the notebook
    # which is where `check_integrity` is being run
    # hence, that cell has ccount is None
    if ccount is None:
        violations.pop()

    if len(violations) > 0:
        logger.warning(f"... cells {violations} were not run consecutively")
    else:
        logger.info("... notebook cells increment at 1: Awesome!")

    return violations  # type: ignore

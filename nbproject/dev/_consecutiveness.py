from typing import Optional

from loguru import logger

from ._notebook import Notebook


def _check_last_cell(nb: Notebook, calling_statement: str) -> bool:
    last_code_cell = None
    for cell in nb.cells:
        if cell["cell_type"] == "code" and cell["source"] != []:
            last_code_cell = cell

    if last_code_cell is not None and calling_statement in "".join(
        last_code_cell["source"]
    ):
        return True
    else:
        return False


def check_consecutiveness(
    nb: Notebook, *, calling_statement: Optional[str] = None
) -> list:
    """Check whether code cells have been executed consecutively.

    Needs to be called in the last code cell of a notebook.
    Otherwise raises `RuntimeError`.

    Returns cell transitions that violate execution at increments of 1 as a list
    of tuples.

    Args:
        nb: Notebook content.
        calling_statement: Statement that calls `check_consecutiveness`.
    """
    if _check_last_cell(nb, calling_statement):  # type: ignore
        raise RuntimeError(
            "Can only check consecutiveness from the last code cell of the notebook."
        )

    cells = nb.cells

    violations = []
    prev = 0

    for cell in cells:
        if cell["cell_type"] != "code" or cell["source"] == []:
            continue

        ccount = cell["execution_count"]
        if ccount is None or ccount - prev != 1:
            violations.append((prev, ccount))

        prev = ccount

    # ignore the very last code cell of the notebook
    # `check_consecutiveness` is being run during publish if `last_cell`` is True
    # hence, that cell has ccount is None
    if ccount is None:
        violations.pop()

    if len(violations) > 0:
        logger.warning(f"Cells {violations} were not run consecutively.")
    else:
        logger.info("Cell numbers increase at increments of 1: Awesome!")

    return violations  # type: ignore

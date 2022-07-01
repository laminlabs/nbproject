from typing import Optional

from ._notebook import Notebook


def check_integrity(
    nb: Notebook, ignore_code: Optional[str] = None
) -> list[tuple[Optional[int], Optional[int]]]:
    """Get current integrity status of the passed notebook.

    Returns list of violations of consecutive execution as tuples of cell numbers.

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

    return violations  # type: ignore

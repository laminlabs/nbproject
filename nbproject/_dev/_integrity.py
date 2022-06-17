from typing import Optional

from ._notebook import Notebook


def check_integrity(nb: Notebook, ignore_code: Optional[str] = None) -> bool:
    cells = nb.cells

    integrity = True
    prev = 0

    for cell in cells:
        if cell["cell_type"] != "code" or cell["source"] == []:
            continue

        if ignore_code is not None and ignore_code in "".join(cell["source"]):
            continue

        ccount = cell["execution_count"]
        if ccount is None or ccount - prev != 1:
            integrity = False
            break

        prev = ccount

    return integrity

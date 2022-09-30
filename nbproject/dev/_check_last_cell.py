from ._notebook import Notebook


def check_last_cell(nb: Notebook, calling_statement: str) -> bool:
    """Check whether code has been executed in the last cell.

    Args:
        nb: Notebook content.
        calling_statement: The statement that calls this function.
    """
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

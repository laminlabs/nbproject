from ._notebook import Notebook


def check_last_cell(nb: Notebook, calling_statement: str) -> bool:
    """Check whether code has been executed in the last cell.

    Args:
        nb: Notebook content.
        calling_statement: The statement that calls this function.
    """
    last_code_cell_source = None
    for cell in nb.cells:
        cell_source = "".join(cell["source"])
        if cell["cell_type"] == "code" and cell_source != "":
            last_code_cell_source = cell_source

    if last_code_cell_source is not None and calling_statement in last_code_cell_source:
        return True
    else:
        return False

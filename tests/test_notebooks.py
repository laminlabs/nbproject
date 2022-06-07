import os
from functools import partial
from pathlib import Path
from signal import SIGTERM
from subprocess import PIPE, Popen
from time import sleep

import orjson

from nbproject._jupyter_communicate import close_session, running_servers, start_session
from nbproject._logger import logger


def kill_process(process):
    if os.name == "nt":
        Popen(f"TASKKILL /F /PID {process.pid} /T")
    else:
        # todo: check if works properly on linux
        os.kill(process.pid, SIGTERM)


def write_cell(msg: dict, cell: dict, ex_count: int):
    if msg["msg_type"] in ("status", "execute_input", "error"):
        return

    cell["execution_count"] = ex_count

    output = {}
    output.update(msg["content"])

    msg_type = msg["msg_type"]
    output["output_type"] = msg_type
    if msg_type == "execute_result":
        output["execution_count"] = ex_count

    if "transient" in output:
        del output["transient"]

    cell["outputs"].append(output)


def execute_notebooks(nb_folder: Path, write: bool = True):
    nb, js = running_servers()
    servers = list(nb) + list(js)
    n_servers = len(servers)

    if n_servers > 1:
        raise Exception("More than 1 server is running.")
    elif n_servers == 0:
        raise Exception("No servers running.")
    else:
        server = servers[0]

    notebooks = nb_folder.glob("**/*.ipynb")

    #  if the last notebook in a subfolder, pytest hangs forever...
    reorder_notebooks = []
    for nb in notebooks:
        if nb.parent == nb_folder:
            reorder_notebooks.append(nb)
        else:
            reorder_notebooks.insert(0, nb)

    for nb in reorder_notebooks:
        nb_name = str(nb.relative_to(nb_folder))
        logger.debug(f"\n\n{nb_name}")

        with open(nb, "rb") as f:
            nb_content = orjson.loads(f.read())

        kernel_name = nb_content["metadata"]["kernelspec"]["name"]

        session, km = start_session(server, nb_name, kernel_name)

        cells = nb_content["cells"]

        ex_count = 1
        for cell in cells:
            if cell["cell_type"] != "code":
                continue
            cell_source = "".join(cell["source"])

            if write:
                output_hook = partial(write_cell, cell=cell, ex_count=ex_count)
            else:
                output_hook = None
            resp = km.execute_interactive(
                cell_source, allow_stdin=False, output_hook=output_hook
            )
            resp_content = resp["content"]
            if resp_content["status"] == "error":
                ename = resp_content["ename"]
                evalue = resp_content["evalue"]

                raise Exception(f"Error {ename} with msg {evalue} in the notebook {nb}")

            ex_count += 1

        close_session(server, session)

        if write:
            with open(nb, "wb") as f:
                f.write(orjson.dumps(nb_content))


def test_notebooks():
    # assuming this is in the tests folder
    nb_folder = Path(__file__).parents[1] / "docs/guides"
    # thread?
    p = Popen(
        ["jupyter", "notebook", str(nb_folder), "--no-browser"],
        stdout=PIPE,
        stderr=PIPE,
    )

    # todo: this should be replaced by check of server availability
    sleep(5)

    try:
        execute_notebooks(nb_folder, write=True)
    except Exception as e:
        kill_process(p)
        raise e

    kill_process(p)
    # pytest hangs for some reason with the following:
    # p.send_signal(CTRL_C_EVENT)

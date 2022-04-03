import os
import nbformat as nbf
from signal import SIGTERM
from pathlib import Path
from subprocess import Popen, PIPE
from time import sleep
from nbproject._jupyter_communicate import start_session, close_session
from nbproject._ipynbname import running_servers


def kill_process(process):
    if os.name == "nt":
        Popen(f"TASKKILL /F /PID {process.pid} /T")
    else:
        # todo: check if works properly on linux
        os.kill(process.pid, SIGTERM)


def test_notebooks():
    # thread?
    p = Popen(
        ["jupyter", "notebook", "../docs/", "--no-browser"], stdout=PIPE, stderr=PIPE
    )

    # todo: this should be replaced by check of server availability
    sleep(5)

    nb, js = running_servers()
    servers = list(nb) + list(js)
    n_servers = len(servers)
    if n_servers > 1:
        kill_process(p)
        raise ValueError("More than 1 server is running.")
    elif n_servers == 0:
        raise ValueError("No servers running.")
    else:
        server = servers[0]

    cwd = Path.cwd()

    notebooks = cwd.glob("../docs/**/*.ipynb")

    for nb in notebooks:
        nb_name = str(nb.relative_to(cwd.parent / "tests/../docs"))

        try:
            nb_content = nbf.read(nb, as_version=nbf.NO_CONVERT)
        except Exception as e:
            kill_process(p)
            raise e

        kernel_name = nb_content["metadata"]["kernelspec"]["name"]

        session, km = start_session(server, nb_name, kernel_name)

        cells = nb_content["cells"]

        for cell in cells:
            if cell["cell_type"] != "code":
                continue
            cell_source = cell["source"]

            resp = km.execute_interactive(cell_source)
            resp_content = resp["content"]
            if resp_content["status"] == "error":
                ename = resp_content["ename"]
                evalue = resp_content["evalue"]

                kill_process(p)
                raise ValueError(
                    f"Error {ename} with msg {evalue} in the notebook {nb}"
                )

        close_session(server, session)

    kill_process(p)
    # pytest hangs for some reason with the following:
    # p.send_signal(CTRL_C_EVENT)

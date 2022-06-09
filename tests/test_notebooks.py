import os
from pathlib import Path
from signal import SIGTERM
from subprocess import PIPE, Popen
from time import sleep

from nbproject._jupyter_communicate import execute_notebooks


def kill_process(process):
    if os.name == "nt":
        Popen(f"TASKKILL /F /PID {process.pid} /T")
    else:
        # todo: check if works properly on linux
        os.kill(process.pid, SIGTERM)


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
        execute_notebooks(nb_folder, write=False)
    except Exception as e:
        kill_process(p)
        raise e

    kill_process(p)
    # pytest hangs for some reason with the following:
    # p.send_signal(CTRL_C_EVENT)

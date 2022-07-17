from pathlib import Path
from subprocess import PIPE, Popen
from typing import Optional, Sequence

from nbproject._logger import logger
from nbproject._schemas import NBRecord, public_fields
from nbproject.dev import read_notebook, write_notebook


def check_notebooks(nb_folder: Path, cleanup: Optional[Sequence] = None):
    if cleanup is None:
        cleanup = []

    notebooks = nb_folder.glob("**/*.ipynb")

    for nb in notebooks:
        nb_content = read_notebook(nb)

        nb_record = NBRecord(nb_content)
        if not nb_record._filled:
            raise Exception(f"No nbproject metadata present in {nb}.")

        fields = public_fields(nb_record)
        nbproj_metadata = nb_content.metadata["nbproject"]
        for field in fields:
            if field not in nbproj_metadata:
                raise Exception(f"No field {field} in the nbproject metadata.")

        if nb.name in cleanup:
            del nb_content.metadata["nbproject"]
            write_notebook(nb_content, nb)


def test_cli():
    main_folder = Path(__file__).parents[1] / "docs"
    folders = ["guides/example-project-uninitialized", "guides/example-project"]

    commands = dict(
        sync_noinit=["sync", "."],
        reqs_noinit=["reqs", "."],
        init=["init"],
        sync=["sync", "."],
        sync_list=["sync"],
        sync_d_nv=["sync", ".", "-d", "-nv"],
        sync_d=["sync", ".", "-d"],
        reqs_list=["reqs"],
        reqs=["reqs", "."],
        publish=["publish", "."],
    )

    for folder in folders:
        nb_folder = main_folder / folder
        logger.debug(f"\n{nb_folder}")

        for cmd_name, cmd in commands.items():
            if "list" in cmd_name:
                files = [str(file) for file in nb_folder.glob("./*") if file.is_file()]
                cmd = cmd + files

            p = Popen(
                ["python", "-m", "nbproject"] + cmd,
                stdout=PIPE,
                stderr=PIPE,
                cwd=nb_folder,
            )
            ecode = p.wait()

            logger.debug(f"\n {cmd_name} exitcode: {ecode}.")
            logger.debug(p.stdout.read().decode())
            logger.debug(p.stderr.read().decode())

            if ecode != 0:
                raise Exception(
                    f"Something happened with the cli command {cmd_name}, the exit code"
                    f" is {ecode}."
                )

        check_notebooks(nb_folder)

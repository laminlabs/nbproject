import nbformat as nbf
from typing import Optional, Sequence
from pathlib import Path
from subprocess import Popen, PIPE
from nbproject._schemas import NBRecord, public_fields
from nbproject._logger import logger


def check_notebooks(nb_folder: Path, ignore_cleanup: Optional[Sequence] = None):
    if ignore_cleanup is None:
        ignore_cleanup = []

    notebooks = nb_folder.glob("**/*.ipynb")

    for nb in notebooks:
        nb_content = nbf.read(nb, as_version=nbf.NO_CONVERT)

        nb_record = NBRecord(nb_content)
        if not nb_record._filled:
            raise Exception(f"No nbproject metadata present in {nb}.")

        fields = public_fields(nb_record)
        nbproj_metadata = nb_content.metadata["nbproject"]
        for field in fields:
            if field not in nbproj_metadata:
                raise Exception(f"No field {field} in the nbproject metadata.")

        if nb.name not in ignore_cleanup:
            del nb_content.metadata["nbproject"]
            nbf.write(nb_content, nb)


def test_cli():
    nb_folder = Path(__file__).parents[1] / "docs/guides"

    commands = dict(init=["init"], sync=["sync", "."])

    for cmd_name, cmd in commands.items():
        p = Popen(
            ["python", "-m", "nbproject"] + cmd, stdout=PIPE, stderr=PIPE, cwd=nb_folder
        )
        ecode = p.wait()

        logger.debug(f"\n {cmd_name} exitcode: {ecode}.")
        logger.debug(p.stdout.read().decode())
        logger.debug(p.stderr.read().decode())

        if ecode != 0:
            raise Exception(
                f"Something happened with the cli command {cmd_name}, the exit code is"
                f" {ecode}."
            )

    check_notebooks(
        nb_folder,
        ignore_cleanup=["example-after-init.ipynb", "2022-05-13-my-task-x.ipynb"],
    )

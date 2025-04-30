import subprocess
from pathlib import Path


def test_running_via_nbconvert():
    result = subprocess.run(
        "jupyter nbconvert --to notebook --execute ./tests/for-nbconvert.ipynb",
        shell=True,
        capture_output=True,
    )
    assert result.returncode == 1
    assert (
        "Please execute notebook 'nbconvert' by passing option '--inplace'."
        in result.stderr.decode()
    )

    result = subprocess.run(
        "jupyter nbconvert --to notebook --inplace --execute ./tests/for-nbconvert.ipynb",
        shell=True,
        capture_output=True,
    )
    print(result.stdout.decode())
    print(result.stderr.decode())
    assert result.returncode == 0

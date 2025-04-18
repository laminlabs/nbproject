import subprocess
from pathlib import Path


def test_running_via_nbconvert():
    result = subprocess.run(
        "jupyter nbconvert --to notebook --execute ./tests/for-nbconvert.ipynb",
        shell=True,
        capture_output=True,
    )
    print(result.stdout.decode())
    print(result.stderr.decode())
    assert result.returncode == 0

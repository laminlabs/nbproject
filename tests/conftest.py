from pathlib import Path


def pytest_collection_modifyitems(session, config, items):
    # make sure that cli is executed first
    cli_idx = 0
    for i, item in enumerate(items):
        if item.name == "test_cli":
            cli_idx = i

    # if not in the list or the first already, then ignore
    if cli_idx != 0:
        items[0], items[cli_idx] = items[cli_idx], items[0]


def pytest_sessionfinish(session, exitstatus):
    test_cli_folder = Path(__file__).parents[1] / "docs/guides/"

    nbproj_file = (
        test_cli_folder / "example-project-uninitialized/nbproject_metadata.yml"
    )
    if nbproj_file.is_file():
        nbproj_file.unlink()

    reqs_subfolders = ["example-project-uninitialized/", "example-project/"]
    for reqs_subfolder in reqs_subfolders:
        reqs_file = test_cli_folder / (reqs_subfolder + "requirments.txt")
        if reqs_file.is_file():
            reqs_file.unlink()

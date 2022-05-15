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
    nbproj_file = Path(__file__).parents[1] / "docs/guides/nbproject_metadata.yml"
    nbproj_file.unlink(missing_ok=True)

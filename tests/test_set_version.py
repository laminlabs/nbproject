from nbproject.dev._set_version import set_version


def test_set_version():
    # all remaining lines are covered in notebooks
    assert set_version(None, "1.2") == "manual-version"

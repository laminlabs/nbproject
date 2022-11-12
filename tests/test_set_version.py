from nbproject.dev._set_version import set_version


def test_set_version():
    # all remaining lines are covered in notebooks
    assert set_version(None, "1.2") == "1.2"
    assert set_version(None, "0") == "0"
    assert set_version(None, "1") == "1"
    assert set_version("1.2.3", "0") == "1.2.3"

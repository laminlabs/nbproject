from collections import namedtuple


def lamin_user_settings():
    """Returns user settings."""
    try:
        from lndb_setup import settings

        return settings.user
    except ImportError:
        MockUserSettings = namedtuple("MockUserSettings", ["id", "handle", "name"])
        return MockUserSettings(id=None, handle=None, name=None)

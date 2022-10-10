def lamin_user_settings():
    """Returns user settings."""
    try:
        from lndb_setup import settings

        return settings.user
    except ImportError:
        return None, None, None

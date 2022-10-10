def lamin_user_settings():
    try:
        from lndb_setup import settings

        return settings.user.handle, settings.user.id
    except ModuleNotFoundError:
        return None, None

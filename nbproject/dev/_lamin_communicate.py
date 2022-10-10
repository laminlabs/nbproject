from typing import Optional


def lamin_user_settings():
    try:
        from lndb_setup import settings

        return settings.user.handle, settings.user.id
    except ImportError:
        return None, None


def lamin_user_name(user_id: Optional[str] = None):
    try:
        import lndb_setup
        import lnschema_core as schema_core
        import sqlmodel as sqm

        settings = lndb_setup.settings

        if settings.instance.name is not None:
            if user_id is None:
                current_user_id = settings.user.id
                if current_user_id is None:
                    return None
                else:
                    user_id = current_user_id

            with sqm.Session(settings.instance.db_engine()) as session:
                user = session.get(schema_core.user, user_id)
                return getattr(user, "name", None)
    except ImportError:
        return None

from pathlib import Path
from typing import Union

from .dev._jupyter_communicate import notebook_path
from .dev._meta_live import MetaLive
from .dev._meta_store import MetaContainer, MetaStore
from .dev._notebook import read_notebook


# https://stackoverflow.com/questions/128573/using-property-on-classmethods/64738850#64738850
class classproperty(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class meta:
    """Access `meta.store` and `meta.live`.

    - `meta.store` - nbproject metadata of the ipynb file, see
      :class:`~nbproject.dev.MetaStore`
    - `meta.live` - execution info and properties derived from notebook content,
      see :class:`~nbproject.dev.MetaLive`

    `meta` is a static class and behaves like a module (no need to initialize it).
    """

    _filepath: Union[str, Path, None] = None
    _env = None
    _time_run = None

    _store: Union[MetaStore, None] = None
    _live: Union[MetaLive, None] = None

    @classmethod
    def _init_meta(cls):
        from ._header import _env, _filepath, _time_run

        env = _env
        filepath = _filepath
        filepath_env = _filepath, _env

        if filepath is None:
            filepath_env = notebook_path(return_env=True)
            if filepath_env is None:
                filepath_env = None, None
            filepath = filepath_env[0]

        if env is None:
            env = filepath_env[1]

        cls._filepath = filepath
        cls._env = env
        cls._time_run = _time_run

        nb_meta = read_notebook(cls._filepath).metadata

        if nb_meta is not None and "nbproject" in nb_meta:
            meta_container = MetaContainer(**nb_meta["nbproject"])
        else:
            empty = "not initialized"
            meta_container = MetaContainer(id=empty, time_init=empty, version=empty)

        cls._store = MetaStore(meta_container, cls._filepath, cls._env)
        cls._live = MetaLive(cls._filepath, cls._time_run, cls._env)

    @classproperty
    def store(cls) -> MetaStore:
        """Metadata stored in the notebook."""
        if cls._store is None:
            cls._init_meta()
        return cls._store  # type: ignore

    @classproperty
    def live(cls) -> MetaLive:
        """Contains execution info and properties of the notebook content."""
        if cls._live is None:
            cls._init_meta()
        return cls._live  # type: ignore

    def __repr__(self):
        return (
            "Metadata object with .live and .store metadata fields:\n"
            f"  .store: {self.store}\n"
            f"  .live: {self.live}"
        )

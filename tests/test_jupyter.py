from pytest import raises

from nbproject.dev._jupyter_communicate import (
    notebook_path,
    prepare_url,
    query_server,
    running_servers,
)
from nbproject.dev._jupyter_lab_commands import _reload_notebook, _save_notebook


def test_jupyter_not_running():
    assert notebook_path() is None
    assert notebook_path(return_env=True) is None

    servers_nbapp, servers_juserv = running_servers()
    assert list(servers_nbapp) == []
    assert list(servers_juserv) == []

    server = dict(token="test", url="localhost/")

    assert (
        prepare_url(server, "/test_query")
        == "localhost/api/sessions/test_query?token=test"  # noqa
    )

    with raises(Exception) as e_info:
        query_server(server)

    assert (
        e_info.value.args[0]
        == "Unable to access server;\nipynbname requires either no security or token"  # noqa
        " based security."
    )


def test_juplab_nothing_happens():
    _save_notebook()
    _reload_notebook()

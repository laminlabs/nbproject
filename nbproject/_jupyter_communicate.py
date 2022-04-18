import json
from pathlib import PurePath
from itertools import chain
from urllib import request

DIR_KEYS = ("notebook_dir", "root_dir")


def prepare_url(server: dict, query_str: str = ""):
    token = server["token"]
    if token:
        query_str = f"{query_str}?token={token}"
    url = f"{server['url']}api/sessions{query_str}"

    return url


def query_server(server: dict):
    # based on https://github.com/msm1089/ipynbname
    try:
        url = prepare_url(server)
        with request.urlopen(url) as req:
            return json.load(req)
    except Exception:
        CONN_ERROR = (
            "Unable to access server;\n"
            + "ipynbname requires either no security or token based security."
        )
        raise Exception(CONN_ERROR)


def running_servers():
    try:
        from notebook.notebookapp import list_running_servers

        servers_nbapp = list_running_servers()
    except ModuleNotFoundError:
        servers_nbapp = []

    try:
        from jupyter_server.serverapp import list_running_servers

        servers_juserv = list_running_servers()
    except ModuleNotFoundError:
        servers_juserv = []

    return servers_nbapp, servers_juserv


def notebook_path():

    servers_nbapp, servers_juserv = running_servers()

    # no running servers
    if servers_nbapp == [] and servers_juserv == []:
        return None

    try:
        from IPython import get_ipython
    except ModuleNotFoundError:
        return None

    ipython_instance = get_ipython()

    # not in an ipython kernel
    if ipython_instance is None:
        return None

    config = ipython_instance.config
    # not in a jupyter notebook
    if "IPKernelApp" not in config:
        return None

    kernel_id = (
        config["IPKernelApp"]["connection_file"].partition("-")[2].split(".", -1)[0]
    )

    for server in chain(servers_nbapp, servers_juserv):
        session = query_server(server)
        for notebook in session:
            if notebook["kernel"]["id"] == kernel_id:
                for dir_key in DIR_KEYS:
                    if dir_key in server:
                        return PurePath(server[dir_key]) / notebook["notebook"]["path"]

    return None


def start_session(server: dict, nb_name: str, kernel_name: str = "python3"):
    from jupyter_client import find_connection_file, BlockingKernelClient

    data = dict(type="notebook", path=nb_name, kernel={"name": kernel_name})
    data = json.dumps(data).encode("utf-8")

    url = prepare_url(server)
    req = request.Request(url, data=data)
    with request.urlopen(req) as resp:
        session = json.load(resp)

    kernel_id = session["kernel"]["id"]

    cf = find_connection_file(kernel_id)
    km = BlockingKernelClient()
    km.load_connection_file(connection_file=cf)

    return session, km


def close_session(server: dict, session: dict):
    session_id = session["id"]

    url = prepare_url(server, "/" + session_id)
    req = request.Request(url, method="DELETE")
    request.urlopen(req)

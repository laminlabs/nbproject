from functools import partial
from itertools import chain
from pathlib import Path, PurePath
from urllib import request

import orjson

from nbproject._logger import logger

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
            return orjson.loads(req.read())
    except Exception:
        CONN_ERROR = (
            "Unable to access server;\n"
            "ipynbname requires either no security or token based security."
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


def notebook_path(return_env=False):

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
                        nb_path = (
                            PurePath(server[dir_key]) / notebook["notebook"]["path"]
                        )
                        if return_env:
                            return (
                                nb_path,
                                "lab" if dir_key == "root_dir" else "notebook",
                            )
                        else:
                            return nb_path

    return None


def start_session(server: dict, nb_name: str, kernel_name: str = "python3"):
    from jupyter_client import BlockingKernelClient, find_connection_file

    data = dict(type="notebook", path=nb_name, kernel={"name": kernel_name})
    data = orjson.dumps(data)

    url = prepare_url(server)
    req = request.Request(url, data=data)  # type: ignore
    with request.urlopen(req) as resp:
        session = orjson.loads(resp.read())

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


def write_cell(msg: dict, cell: dict, ex_count: int):
    if msg["msg_type"] in ("status", "execute_input", "error"):
        return

    cell["execution_count"] = ex_count

    output = {}
    output.update(msg["content"])

    msg_type = msg["msg_type"]
    output["output_type"] = msg_type
    if msg_type == "execute_result":
        output["execution_count"] = ex_count

    if "transient" in output:
        del output["transient"]

    cell["outputs"].append(output)


def execute_notebooks(nb_folder: Path, write: bool = True):

    nb, js = running_servers()
    servers = list(nb) + list(js)
    n_servers = len(servers)

    if n_servers > 1:
        print(servers)
        raise Exception("More than 1 server is running.")
    elif n_servers == 0:
        raise Exception("No servers running.")
    else:
        server = servers[0]

    notebooks = nb_folder.glob("**/*.ipynb")

    for nb in notebooks:
        nb_name = str(nb.relative_to(nb_folder))
        logger.debug(f"\n\n{nb_name}")

        with open(nb, "rb") as f:
            nb_content = orjson.loads(f.read())

        kernel_name = nb_content["metadata"]["kernelspec"]["name"]

        session, km = start_session(server, nb_name, kernel_name)

        cells = nb_content["cells"]

        ex_count = 1
        for cell in cells:
            if cell["cell_type"] != "code":
                continue
            cell_source = "".join(cell["source"])

            if write:
                output_hook = partial(write_cell, cell=cell, ex_count=ex_count)
            else:
                output_hook = None
            resp = km.execute_interactive(
                cell_source, allow_stdin=False, output_hook=output_hook
            )
            resp_content = resp["content"]
            if resp_content["status"] == "error":
                ename = resp_content["ename"]
                evalue = resp_content["evalue"]

                raise Exception(f"Error {ename} with msg {evalue} in the notebook {nb}")

            ex_count += 1

        close_session(server, session)

        if write:
            with open(nb, "wb") as f:
                f.write(orjson.dumps(nb_content))

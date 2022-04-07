import json
from jupyter_client import find_connection_file, BlockingKernelClient
from urllib import request

from ._ipynbname import prepare_url


def start_session(server: dict, nb_name: str, kernel_name: str = "python3"):
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

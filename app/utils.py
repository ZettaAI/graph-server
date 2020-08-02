from typing import Iterable

from pychunkedgraph.graph import ChunkedGraph

CACHE = {}


def _get_bigtable_client_info():
    from os import environ
    from pychunkedgraph.graph.meta import BigTableConfig

    kwargs = {
        "PROJECT": environ.get("BIGTABLE_PROJECT", "zetta-lee-fly-vnc-001"),
        "INSTANCE": environ.get("BIGTABLE_INSTANCE", "zetta-lee-fly-vnc-graph-test"),
        "ADMIN": False,  # TODO make these dynamic (low-priority)
        "READ_ONLY": False,
    }
    return BigTableConfig(**kwargs)


def _get_cg_backend_client_info():
    from pychunkedgraph.graph.meta import BackendClientInfo

    # only BigTable is supported at this time.
    return BackendClientInfo(TYPE="bigtable", CONFIG=_get_bigtable_client_info())


def get_cg(graph_id: str) -> ChunkedGraph:
    try:
        return CACHE[graph_id]
    except KeyError:
        pass
    CACHE[graph_id] = ChunkedGraph(
        graph_id=graph_id, client_info=_get_cg_backend_client_info()
    )
    return CACHE[graph_id]


async def get_info(graph_id: str) -> dict:
    cg = get_cg(graph_id)
    dataset_info = cg.meta.dataset_info
    app_info = {"app": {"supported_api_versions": [0, 1]}}
    info = {**dataset_info, **app_info}
    info["sharded_mesh"] = True
    info["mesh"] = cg.meta.custom_data.get("mesh", {}).get("dir", "graphene_meshes")
    return info


def string_array(a: Iterable) -> Iterable:
    from numpy import char

    return char.mod("%d", a).tolist()


def toboolean(value):
    """ Parse value to boolean type. """
    if not value:
        raise ValueError("Can't convert null to boolean")

    if isinstance(value, bool):
        return value
    try:
        value = value.lower()
    except:
        raise ValueError(f"Can't convert {value} to boolean")

    if value in ("true", "1"):
        return True
    if value in ("false", "0"):
        return False

    raise ValueError(f"Can't convert {value} to boolean")

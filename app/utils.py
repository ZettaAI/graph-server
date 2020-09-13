from typing import Iterable

from pychunkedgraph.graph import ChunkedGraph

CACHE = {}


def get_datasets():
    from glob import glob
    from yaml import safe_load
    from yaml import YAMLError
    from pychunkedgraph.graph.client import BackendClientInfo
    from pychunkedgraph.graph.client.bigtable import BigTableConfig

    datasets = []
    for f in glob("/app/datasets/*.yml"):
        config = None
        with open(f, "r") as stream:
            try:
                config = safe_load(stream)
            except YAMLError as exc:
                raise (exc)
        client_info = BackendClientInfo(
            config["backend_client"]["TYPE"],
            CONFIG=BigTableConfig(**config["backend_client"]["CONFIG"]),
        )
        datasets.append((config["graph_id"], client_info))
    return datasets


def preload_datasets():
    from pychunkedgraph.graph.utils.context_managers import TimeIt

    for dataset in get_datasets():
        graph_id, client_info = dataset
        with TimeIt(f"preloading {graph_id}"):
            CACHE[graph_id] = ChunkedGraph(graph_id=graph_id, client_info=client_info)
            # trigger CloudVolume initialization as well
            print(f"layer count {CACHE[graph_id].meta.layer_count}")


def get_cg(graph_id: str) -> ChunkedGraph:
    from pychunkedgraph.graph.client import get_default_client_info

    try:
        return CACHE[graph_id]
    except KeyError:
        pass
    CACHE[graph_id] = ChunkedGraph(
        graph_id=graph_id, client_info=get_default_client_info()
    )
    return CACHE[graph_id]


async def get_info(graph_id: str) -> dict:
    cg = get_cg(graph_id)
    dataset_info = cg.meta.dataset_info
    app_info = {"app": {"supported_api_versions": [0, 1]}}
    info = {**dataset_info, **app_info}
    info["graph"]["chunk_size"] = [1024, 512, 128]
    info["graph"]["bounding_box"] = [1024, 512, 128]
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

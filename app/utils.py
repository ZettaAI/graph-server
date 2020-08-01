from typing import Iterable

from pychunkedgraph.graph import ChunkedGraph


CACHE = {}


# def get_bigtable_client(config):
#     project_id = config.get("PROJECT_ID", None)
#     if config.get("emulate", False):
#         credentials = DoNothingCreds()
#     elif project_id is not None:
#         credentials, _ = default_creds()
#     else:
#         credentials, project_id = default_creds()

#     client = bigtable.Client(admin=True, project=project_id, credentials=credentials)
#     return client


def get_cg(graph_id: str) -> ChunkedGraph:
    try:
        return CACHE[graph_id]
    except KeyError:
        pass
    CACHE[graph_id] = ChunkedGraph(graph_id=graph_id)
    return CACHE[graph_id]


async def get_info(graph_id: str) -> dict:
    cg = get_cg(graph_id)
    dataset_info = cg.meta.dataset_info
    app_info = {"app": {"supported_api_versions": [0, 1]}}
    info = {**dataset_info, **app_info}
    info["sharded_mesh"] = True
    info["verify_mesh"] = cg.meta.custom_data.get("mesh", {}).get("verify", False)
    info["mesh"] = cg.meta.custom_data.get("mesh", {}).get("dir", "graphene_meshes")
    return info


def string_array(a: Iterable) -> Iterable:
    from numpy import char

    return char.mod("%d", a).tolist()

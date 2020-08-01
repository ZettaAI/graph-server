from pychunkedgraph.graph import ChunkedGraph


CACHE = {}


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

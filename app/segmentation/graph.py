from ..utils import get_cg


async def get_root(graph_id: str, node_id: int):
    cg = get_cg(graph_id)
    return cg.get_root(node_id)


async def get_leaves(graph_id: str, node_id: int, bounds: str):
    from numpy import array

    bbox = None
    if bounds:
        bbox = array([b.split("-") for b in bounds.split("_")], dtype=int).T

    return get_cg(graph_id).get_subgraph(
        node_id, bbox=bbox, bbox_is_coordinate=True, leaves_only=True
    )

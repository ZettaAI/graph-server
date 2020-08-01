"""
Leaves and edges of an agglomeration, within (optional) bounding box.
"""

from typing import Optional

from numpy import array

from . import api
from . import get_cg
from . import string_array


@api.get("/table/{graph_id}/node/{node_id}/subgraph")
async def subgraph(
    graph_id: str,
    node_id: int,
    bounds: Optional[str] = "",
    int64_as_str: Optional[bool] = True,
):
    bbox = None
    if bounds:
        bbox = array([b.split("-") for b in bounds.split("_")], dtype=int).T
    atomic_edges = get_cg(graph_id).get_subgraph(
        node_id, bbox=bbox, bbox_is_coordinate=True
    )
    if int64_as_str:
        return {"atomic_edges": string_array(atomic_edges)}
    return {"atomic_edges": atomic_edges}


@api.get("/table/{graph_id}/node/{node_id}/leaves")
async def leaves(
    graph_id: str,
    node_id: int,
    bounds: Optional[str] = "",
    int64_as_str: Optional[bool] = True,
):
    bbox = None
    if bounds:
        bbox = array([b.split("-") for b in bounds.split("_")], dtype=int).T
    leaves = get_cg(graph_id).get_subgraph(
        node_id, bbox=bbox, bbox_is_coordinate=True, leaves_only=True
    )
    if int64_as_str:
        return {"leaf_ids": string_array(leaves)}
    return {"leaf_ids": leaves}

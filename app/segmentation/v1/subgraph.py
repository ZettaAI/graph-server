"""
Leaves and edges of an agglomeration, within (optional) bounding box.
"""

from typing import Optional

from numpy import array
from fastapi import Request
from fastapi import APIRouter

from ...utils import get_cg
from ...utils import string_array


router = APIRouter()


@router.get("/{graph_id}/node/{node_id}/subgraph")
async def subgraph(
    graph_id: str,
    node_id: int,
    bounds: Optional[str] = "",
    int64_as_str: Optional[bool] = False,
):
    bbox = None
    if bounds:
        bbox = array([b.split("-") for b in bounds.split("_")], dtype=int).T
    atomic_edges = get_cg(graph_id).get_subgraph(
        node_id, bbox=bbox, bbox_is_coordinate=True, edges_only=True
    )
    if int64_as_str:
        return {"atomic_edges": string_array(atomic_edges)}
    return {"atomic_edges": atomic_edges.tolist()}


@router.get("/{graph_id}/node/{node_id}/leaves")
async def leaves(
    graph_id: str,
    node_id: int,
    bounds: Optional[str] = "",
    int64_as_str: Optional[bool] = False,
):
    bbox = None
    if bounds:
        bbox = array([b.split("-") for b in bounds.split("_")], dtype=int).T
    leaves = get_cg(graph_id).get_subgraph(
        node_id, bbox=bbox, bbox_is_coordinate=True, leaves_only=True
    )
    if int64_as_str:
        return {"leaf_ids": string_array(leaves)}
    return {"leaf_ids": leaves.tolist()}


@router.get("/{graph_id}/node/{node_id}/leaves_many")
async def leaves_many(
    request: Request,
    graph_id: str,
    bounds: Optional[str] = "",
    int64_as_str: Optional[bool] = False,
):
    from numpy import uint64
    from numpy import frombuffer

    bbox = None
    if bounds:
        bbox = array([b.split("-") for b in bounds.split("_")], dtype=int).T
    root_ids = frombuffer(await request.body(), uint64)
    root_to_leaves_mapping = get_cg(graph_id).get_subgraph_nodes(
        root_ids,
        bbox=bbox,
        bbox_is_coordinate=True,
        return_layers=[1],
        serializable=True,
    )
    return {"root_to_leaves_mapping": root_to_leaves_mapping}


@router.get("/{graph_id}/node/{node_id}/lvl2_graph")
async def lvl2_graph(
    graph_id: str,
    node_id: int,
    int64_as_str: Optional[bool] = False,
):
    from pychunkedgraph.graph.analysis.pathing import get_lvl2_edge_list

    return {
        "edge_graph": string_array(get_lvl2_edge_list(get_cg(graph_id), int(node_id)))
    }

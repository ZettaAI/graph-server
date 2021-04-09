from typing import Optional

from fastapi import APIRouter
from fastapi import Request
from ...utils import get_cg
from .edits_helpers import _process_node_info

router = APIRouter()


@router.post("/{graph_id}/graph/find_path")
async def find_path(
    request: Request,
    graph_id: str,
    int64_as_str: Optional[bool] = False,
    precision_mode: Optional[bool] = True,
):
    from copy import copy
    from json import loads

    from pychunkedgraph.graph.analysis import pathing
    from pychunkedgraph.meshing import mesh_analysis

    from ...utils import string_array

    cg = copy(get_cg(graph_id))
    nodes = loads(await request.body())
    assert len(nodes) == 2
    supervoxel_ids, _ = _process_node_info(cg, nodes)
    source_supervoxel_id = supervoxel_ids[0]
    target_supervoxel_id = supervoxel_ids[1]
    source_l2_id = cg.get_parent(source_supervoxel_id)
    target_l2_id = cg.get_parent(target_supervoxel_id)

    l2_path = pathing.find_l2_shortest_path(cg, source_l2_id, target_l2_id)
    if int64_as_str:
        l2_path = string_array(l2_path)
    else:
        l2_path = l2_path.tolist()
    if precision_mode:
        centroids, failed_l2_ids = mesh_analysis.compute_mesh_centroids_of_l2_ids(
            cg, l2_path, flatten=True
        )
        for i in range(len(centroids)):
            centroids[i] = centroids[i].tolist()
        if int64_as_str:
            failed_l2_ids = string_array(failed_l2_ids)
        return {
            "centroids_list": centroids,
            "failed_l2_ids": failed_l2_ids,
            "l2_path": l2_path,
        }
    else:
        centroids = pathing.compute_rough_coordinate_path(cg, l2_path)
        for i in range(len(centroids)):
            centroids[i] = centroids[i].tolist()
        return {"centroids_list": centroids, "failed_l2_ids": [], "l2_path": l2_path}
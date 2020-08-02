from typing import Iterable

from pychunkedgraph.graph import ChunkedGraph


def manifest_response(cg: ChunkedGraph, args: tuple):
    from numpy import uint64
    from pychunkedgraph.meshing.manifest import speculative_manifest
    from pychunkedgraph.meshing.manifest import get_highest_child_nodes_with_meshes

    (
        node_id,
        verify,
        return_seg_ids,
        prepend_seg_ids,
        start_layer,
        flexible_start_layer,
        bounding_box,
        data,
    ) = args
    resp = {}
    seg_ids = []
    if not verify:
        seg_ids, resp["fragments"] = speculative_manifest(cg, node_id)
    else:
        seg_ids, resp["fragments"] = get_highest_child_nodes_with_meshes(
            cg,
            uint64(node_id),
            stop_layer=2,
            start_layer=start_layer,
            bounding_box=bounding_box,
            flexible_start_layer=flexible_start_layer,
        )
        if prepend_seg_ids:
            resp["fragments"] = [
                f"~{i}:{f}" for i, f in zip(seg_ids, resp["fragments"])
            ]
        seg_ids = seg_ids.tolist()
    if return_seg_ids:
        resp["seg_ids"] = seg_ids
    return _check_post_options(cg, resp, data, seg_ids)


def _check_post_options(cg: ChunkedGraph, resp: dict, data: dict, seg_ids: Iterable):
    from ..utils import toboolean

    if toboolean(data.get("return_seg_ids", "false")):
        resp["seg_ids"] = seg_ids
    if toboolean(data.get("return_seg_id_layers", "false")):
        resp["seg_id_layers"] = cg.get_chunk_layers(seg_ids)
    if toboolean(data.get("return_seg_chunk_coordinates", "false")):
        resp["seg_chunk_coordinates"] = [
            cg.get_chunk_coordinates(seg_id) for seg_id in seg_ids
        ]
    return resp

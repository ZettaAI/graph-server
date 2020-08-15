from typing import Iterable
from os.path import join

from pychunkedgraph.graph import ChunkedGraph


def _check_post_options(
    cg: ChunkedGraph, resp: dict, data: dict, seg_ids: Iterable
) -> dict:
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


def manifest_response(cg: ChunkedGraph, args: tuple) -> dict:
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


def remesh(cg: ChunkedGraph, operation_id: int, l2ids: Iterable):
    from time import sleep
    from cloudvolume import Storage
    from pychunkedgraph.meshing.meshgen import remeshing

    mesh_dir = cg.meta.dataset_info["mesh"]
    mesh_info = cg.meta.custom_data.get("mesh", {})

    unsharded_mesh_path = join(
        cg.meta.data_source.WATERSHED,
        mesh_dir,
        cg.meta.dataset_info["mesh_metadata"]["unsharded_mesh_dir"],
    )

    # files to keep track of re-meshing tasks
    # deleted after remeshing was successfult
    in_progress = f"{unsharded_mesh_path}/in-progress"
    with Storage(in_progress) as storage:  # pylint: disable=not-context-manager
        storage.put_file(
            file_path=f"{operation_id}",
            content=l2ids.tobytes(),
            cache_control="public",
        )
    # TODO delete
    print(f"{cg.graph_id} {operation_id} {l2ids}")
    return f"{cg.graph_id} {operation_id} {l2ids}"

    remeshing(
        cg,
        l2ids,
        stop_layer=mesh_info["max_layer"],
        mip=mesh_info["mip"],
        max_err=mesh_info["max_error"],
        cv_sharded_mesh_dir=mesh_dir,
        cv_unsharded_mesh_path=unsharded_mesh_path,
    )

    with Storage(in_progress) as storage:  # pylint: disable=not-context-manager
        storage.delete_file(f"{operation_id}")


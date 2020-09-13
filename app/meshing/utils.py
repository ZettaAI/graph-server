from typing import Tuple
from typing import Iterable
from os.path import join

from numpy import uint64
from numpy import ndarray
from cloudvolume import Storage

from pychunkedgraph.graph import ChunkedGraph
from pychunkedgraph.meshing.meshgen import remeshing

REMESH_PREFIX = "remesh_"


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


def get_remesh_info(cg: ChunkedGraph, operation_id: int) -> Tuple[str, str, str, str]:
    mesh_dir = cg.meta.dataset_info["mesh"]
    unsharded_mesh_path = join(
        cg.meta.data_source.WATERSHED,
        mesh_dir,
        cg.meta.dataset_info["mesh_metadata"]["unsharded_mesh_dir"],
    )

    return (
        mesh_dir,
        unsharded_mesh_path,
        f"{unsharded_mesh_path}/in-progress",
        f"{REMESH_PREFIX}{operation_id}",
    )


def record_remesh_ids(cg: ChunkedGraph, operation_id: int, l2ids: ndarray):
    from cloudvolume.storage import SimpleStorage as Storage

    _, _, bucket_path, file_name = get_remesh_info(cg, operation_id)
    with Storage(bucket_path) as storage:  # pylint: disable=not-context-manager
        storage.put_file(file_path=file_name, content=l2ids.tobytes())


def remesh(cg: ChunkedGraph, operation_id: int, l2ids: ndarray):
    from cloudvolume.storage import SimpleStorage as Storage

    mesh_info = cg.meta.custom_data.get("mesh", {})
    mesh_dir, unsharded_mesh_path, bucket_path, file_name = get_remesh_info(
        cg, operation_id
    )

    remeshing(
        cg,
        l2ids,
        stop_layer=mesh_info["max_layer"],
        mip=mesh_info["mip"],
        max_err=mesh_info["max_error"],
        cv_sharded_mesh_dir=mesh_dir,
        cv_unsharded_mesh_path=unsharded_mesh_path,
    )
    with Storage(bucket_path) as storage:  # pylint: disable=not-context-manager
        storage.delete_file(file_name)


def _get_pending_tasks(pending_path: str) -> list:
    from numpy import frombuffer

    tasks = []
    with Storage(pending_path) as storage:  # pylint: disable=not-context-manager
        for f in storage.get_files(list(storage.list_files(prefix=REMESH_PREFIX))):
            tasks.append((f["filename"], frombuffer(f["content"], dtype=uint64)))
    return tasks


def remesh_pending(cg: ChunkedGraph):
    mesh_dir = cg.meta.dataset_info["mesh"]
    mesh_info = cg.meta.custom_data.get("mesh", {})
    unsharded_mesh_path = join(
        cg.meta.data_source.WATERSHED,
        mesh_dir,
        cg.meta.dataset_info["mesh_metadata"]["unsharded_mesh_dir"],
    )

    pending_path = f"{unsharded_mesh_path}/in-progress"
    for task in _get_pending_tasks(pending_path):
        fname, l2ids = task
        remeshing(
            cg,
            l2ids,
            stop_layer=mesh_info["max_layer"],
            mip=mesh_info["mip"],
            max_err=mesh_info["max_error"],
            cv_sharded_mesh_dir=mesh_dir,
            cv_unsharded_mesh_path=unsharded_mesh_path,
        )

        with Storage(pending_path) as storage:  # pylint: disable=not-context-manager
            storage.delete_file(fname)

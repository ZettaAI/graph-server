from typing import Tuple
from typing import Iterable
from json import loads

from numpy import array
from numpy import uint64
from fastapi import Request
from pychunkedgraph.graph import exceptions
from pychunkedgraph.graph import ChunkedGraph


def _process_node_info(
    cg: ChunkedGraph, nodes: Iterable[Iterable]
) -> Tuple[list, list]:
    atomic_ids = []
    coords = []
    for node in nodes:
        node_id = node[0]
        x, y, z = node[1:]
        coord = array([x, y, z]) / cg.meta.resolution
        atomic_id = cg.get_atomic_id_from_coord(*coord, parent_id=uint64(node_id))
        assert atomic_id, f"Could not determine supervoxel ID for {coord}."
        coords.append(coord)
        atomic_ids.append(atomic_id)
    return atomic_ids, coords


def _process_split_request_nodes(cg: ChunkedGraph, data: dict) -> dict:
    from collections import defaultdict

    result = {}
    for k in ["sources", "sinks"]:
        result[k] = defaultdict(list)
        result[k]["id"], result[k]["coord"] = _process_node_info(cg, data[k])
    return result


async def merge_helper(cg: ChunkedGraph, request: Request):
    from numpy import all
    from numpy import abs

    nodes = loads(await request.body())
    assert len(nodes) == 2, "Only 2 points can be merged at this time."

    atomic_edge, coords = _process_node_info(cg, nodes)
    # limit merge span to 3 chunks
    coord0 = cg.get_chunk_coordinates(atomic_edge[0])
    coord1 = cg.get_chunk_coordinates(atomic_edge[1])
    assert all(abs(coord0 - coord1) < 4), "Chebyshev distance exceeded, max 3 chunks."

    try:
        ret = cg.add_edges(
            user_id=request.client,
            atomic_edges=array(atomic_edge, dtype=uint64),
            source_coords=coords[:1],
            sink_coords=coords[1:],
        )
    except exceptions.LockingError as e:
        raise exceptions.InternalServerError(e)
    except exceptions.PreconditionError as e:
        raise exceptions.BadRequest(e)

    assert ret.new_root_ids is not None, "Could not merge selected supervoxels."
    # if len(ret.new_lvl2_ids) > 0:
    #     # _remeshing(cg.get_serialized_info(), ret.new_lvl2_ids)
    #     t = threading.Thread(
    #         target=_remeshing, args=(cg.get_serialized_info(), ret.new_lvl2_ids)
    #     )
    #     t.start()
    return ret


async def split_helper(cg: ChunkedGraph, request: Request):
    from collections import defaultdict

    data_dict = _process_split_request_nodes(cg, loads(await request.body()))
    try:
        ret = cg.remove_edges(
            user_id=request.client,
            source_ids=data_dict["sources"]["id"],
            sink_ids=data_dict["sinks"]["id"],
            source_coords=data_dict["sources"]["coord"],
            sink_coords=data_dict["sinks"]["coord"],
            mincut=True,
        )
    except exceptions.LockingError as e:
        raise exceptions.InternalServerError(e)
    except exceptions.PreconditionError as e:
        raise exceptions.BadRequest(e)

    assert ret.new_root_ids is not None, "Could not split selected segment groups."
    # if len(ret.new_lvl2_ids) > 0:
    #     # _remeshing(cg.get_serialized_info(), ret.new_lvl2_ids)
    #     t = threading.Thread(
    #         target=_remeshing, args=(cg.get_serialized_info(), ret.new_lvl2_ids)
    #     )
    #     t.start()
    return ret


async def split_preview_helper(
    cg: ChunkedGraph, request: Request, int64_as_str: bool = False
):
    from collections import defaultdict
    from pychunkedgraph.graph.cutting import run_split_preview
    from . import string_array

    data_dict = _process_split_request_nodes(cg, loads(await request.body()))
    try:
        supervoxel_ccs, illegal_split = run_split_preview(
            cg=cg,
            source_ids=data_dict["sources"]["id"],
            sink_ids=data_dict["sinks"]["id"],
            source_coords=data_dict["sources"]["coord"],
            sink_coords=data_dict["sinks"]["coord"],
            bb_offset=(240, 240, 24),
        )
    except exceptions.PreconditionError as e:
        raise exceptions.BadRequest(e)

    if int64_as_str:
        return {
            "supervoxel_connected_components": string_array(supervoxel_ccs),
            "illegal_split": illegal_split,
        }
    return {
        "supervoxel_connected_components": supervoxel_ccs,
        "illegal_split": illegal_split,
    }


async def undo_helper(cg: ChunkedGraph, request: Request):
    operation_id = uint64(loads(await request.body())["operation_id"])
    try:
        ret = cg.undo(user_id=request.client, operation_id=operation_id)
    except exceptions.LockingError as e:
        raise exceptions.InternalServerError(e)
    except (exceptions.PreconditionError, exceptions.PostconditionError) as e:
        raise exceptions.BadRequest(e)
    # if ret.new_lvl2_ids.size > 0:
    #     # _remeshing(cg.get_serialized_info(), ret.new_lvl2_ids)
    #     t = threading.Thread(
    #         target=_remeshing, args=(cg.get_serialized_info(), ret.new_lvl2_ids)
    #     )
    #     t.start()
    return ret


async def redo_helper(cg: ChunkedGraph, request: Request):
    operation_id = uint64(loads(await request.body())["operation_id"])
    try:
        ret = cg.redo(user_id=request.client, operation_id=operation_id)
    except exceptions.LockingError as e:
        raise exceptions.InternalServerError(e)
    except (exceptions.PreconditionError, exceptions.PostconditionError) as e:
        raise exceptions.BadRequest(e)
    # if ret.new_lvl2_ids.size > 0:
    #     # _remeshing(cg.get_serialized_info(), ret.new_lvl2_ids)
    #     t = threading.Thread(
    #         target=_remeshing, args=(cg.get_serialized_info(), ret.new_lvl2_ids)
    #     )
    #     t.start()
    return ret


def format_edit_result(result, int64_as_str: bool):
    from . import string_array

    if int64_as_str:
        return {
            "operation_id": str(result.operation_id),
            "new_root_ids": string_array(result.new_root_ids),
        }
    return {
        "operation_id": result.operation_id,
        "new_root_ids": result.new_root_ids,
    }
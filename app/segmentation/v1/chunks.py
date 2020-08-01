from datetime import datetime

from pychunkedgraph.graph.attributes import Hierarchy


def _l2_chunk_children(
    graph_id: int, chunk_id: int, timestamp: datetime, flatten: bool = False
):
    from numpy import array
    from numpy import uint64
    from . import get_cg

    cg = get_cg(graph_id)
    chunk_id = uint64(chunk_id)
    chunk_layer = cg.get_chunk_layer(chunk_id)
    assert chunk_layer == 2, f"Chunk layer must be 2, got {chunk_layer}"

    rr_chunk = cg.range_read_chunk(
        chunk_id, properties=Hierarchy.Child, time_stamp=timestamp,
    )

    if flatten:
        l2_chunk_array = []
        for l2 in rr_chunk:
            svs = rr_chunk[l2][0].value
            for sv in svs:
                l2_chunk_array.extend([l2, sv])
        return array(l2_chunk_array)
    else:
        l2_chunk_dict = {}
        for k in rr_chunk:
            l2_chunk_dict[k] = rr_chunk[k][0].value
        return l2_chunk_dict


# @bp.route("/table/<table_id>/l2_chunk_children/<chunk_id>", methods=["GET"])
# @auth_requires_permission("view")
# def handle_l2_chunk_children(table_id, chunk_id):
#     timestamp = datetime.fromtimestamp(timestamp, UTC)
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     as_array = request.args.get("as_array", default=False, type=toboolean)
#     l2_chunk_children = common.handle_l2_chunk_children(table_id, chunk_id, as_array)
#     if as_array:
#         resp = {"l2_chunk_children": l2_chunk_children}
#     else:
#         resp = {"l2_chunk_children": pickle.dumps(l2_chunk_children)}
#     return jsonify_with_kwargs(resp, int64_as_str=int64_as_str)


# ### GET L2:SV MAPPINGS OF A L2 CHUNK BINARY ------------------------------------------------------------------

# @bp.route("/table/<table_id>/l2_chunk_children_binary/<chunk_id>", methods=["GET"])
# @auth_requires_permission("view")
# def handle_l2_chunk_children_binary(table_id, chunk_id):
#     timestamp = datetime.fromtimestamp(timestamp, UTC)
#     as_array = request.args.get("as_array", default=False, type=toboolean)
#     l2_chunk_children = common.handle_l2_chunk_children(table_id, chunk_id, as_array)
#     if as_array:
#         return tobinary(l2_chunk_children)
#     else:
#         return pickle.dumps(l2_chunk_children)


# ### GET L2:SV MAPPINGS OF A L2 CHUNK ------------------------------------------------------------------

# @bp.route("/table/<table_id>/l2_chunk_children/<chunk_id>", methods=["GET"])
# @auth_requires_permission("view")
# def handle_l2_chunk_children(table_id, chunk_id):
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
#     as_array = request.args.get("as_array", default=False, type=toboolean)
#     l2_chunk_children = common.handle_l2_chunk_children(table_id, chunk_id, as_array)
#     if as_array:
#         return tobinary(l2_chunk_children)
#     else:
#         return pickle.dumps(l2_chunk_children)


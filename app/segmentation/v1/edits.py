# ### MERGE ----------------------------------------------------------------------


# @bp.route("/table/<table_id>/merge", methods=["POST"])
# @auth_requires_permission("edit")
# def handle_merge(table_id):
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     merge_result = common.handle_merge(table_id)
#     resp = {"operation_id": merge_result.operation_id, "new_root_ids": merge_result.new_root_ids}
#     return jsonify_with_kwargs(resp, int64_as_str=int64_as_str)


# ### SPLIT ----------------------------------------------------------------------


# @bp.route("/table/<table_id>/split", methods=["POST"])
# @auth_requires_permission("edit")
# def handle_split(table_id):
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     split_result = common.handle_split(table_id)
#     resp = {"operation_id": split_result.operation_id, "new_root_ids": split_result.new_root_ids}
#     return jsonify_with_kwargs(resp, int64_as_str=int64_as_str)


# @bp.route('/table/<table_id>/graph/split_preview', methods=["POST"])
# @auth_requires_permission("view")
# def handle_split_preview(table_id):
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     split_preview = common.handle_split_preview(table_id)
#     return jsonify_with_kwargs(split_preview, int64_as_str=int64_as_str)


# ### UNDO ----------------------------------------------------------------------


# @bp.route("/table/<table_id>/undo", methods=["POST"])
# @auth_requires_permission("edit")
# def handle_undo(table_id):
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     undo_result = common.handle_undo(table_id)
#     resp = {"operation_id": undo_result.operation_id, "new_root_ids": undo_result.new_root_ids}
#     return jsonify_with_kwargs(resp, int64_as_str=int64_as_str)


# ### REDO ----------------------------------------------------------------------


# @bp.route("/table/<table_id>/redo", methods=["POST"])
# @auth_requires_permission("edit")
# def handle_redo(table_id):
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     redo_result = common.handle_redo(table_id)
#     resp = {"operation_id": redo_result.operation_id, "new_root_ids": redo_result.new_root_ids}
#     return jsonify_with_kwargs(resp, int64_as_str=int64_as_str)

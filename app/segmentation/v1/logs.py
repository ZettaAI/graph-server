# @bp.route("/table/<table_id>/change_log", methods=["GET"])
# @auth_requires_admin
# def change_log_full(table_id):
#     si = io.StringIO()
#     cw = csv.writer(si)
#     log_entries = common.change_log(table_id)
#     cw.writerow(["user_id","action","root_ids","timestamp"])
#     cw.writerows(log_entries)
#     output = make_response(si.getvalue())
#     output.headers["Content-Disposition"] = f"attachment; filename={table_id}.csv"
#     output.headers["Content-type"] = "text/csv"
#     return output


# @bp.route("/table/<table_id>/tabular_change_log_recent", methods=["GET"])
# @auth_requires_permission("view") #TODO: admin_view
# def tabular_change_log_weekly(table_id):
#     disp = request.args.get("disp", default=False, type=toboolean)
#     weekly_tab_change_log = common.tabular_change_log_recent(table_id)

#     if disp:
#         return weekly_tab_change_log.to_html()
#     else:
#         return weekly_tab_change_log.to_json()


# @bp.route("/table/<table_id>/root/<root_id>/change_log", methods=["GET"])
# @auth_requires_permission("view")
# def change_log(table_id, root_id):
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     log = common.change_log(table_id, root_id)
#     return jsonify_with_kwargs(log, int64_as_str=int64_as_str)


# @bp.route("/table/<table_id>/root/<root_id>/tabular_change_log", methods=["GET"])
# @auth_requires_permission("view")
# def tabular_change_log(table_id, root_id):
#     disp = request.args.get("disp", default=False, type=toboolean)
#     tab_change_log = common.tabular_change_log(table_id, root_id)

#     if disp:
#         return tab_change_log.to_html()
#     else:
#         return tab_change_log.to_json()

# @bp.route("/table/<table_id>/root/<root_id>/merge_log", methods=["GET"])
# @auth_requires_permission("view")
# def merge_log(table_id, root_id):
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     log = common.merge_log(table_id, root_id)
#     return jsonify_with_kwargs(log, int64_as_str=int64_as_str)


# @bp.route("/table/<table_id>/oldest_timestamp", methods=["GET"])
# @auth_requires_permission("view")
# def oldest_timestamp(table_id):
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     delimiter = request.args.get("delimiter", default=" ", type=str)
#     earliest_timestamp = common.oldest_timestamp(table_id)
#     resp = {"iso": earliest_timestamp.isoformat(delimiter)}
#     return jsonify_with_kwargs(resp, int64_as_str=int64_as_str)


# @bp.route("/table/<table_id>/root/<root_id>/last_edit", methods=["GET"])
# @auth_requires_permission("view")
# def last_edit(table_id, root_id):
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     delimiter = request.args.get("delimiter", default=" ", type=str)
#     latest_timestamp = common.last_edit(table_id, root_id)
#     resp = {"iso": latest_timestamp.isoformat(delimiter)}
#     return jsonify_with_kwargs(resp, int64_as_str=int64_as_str)


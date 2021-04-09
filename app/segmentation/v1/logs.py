"""
Various change log endpoints.
"""

from typing import Optional
from typing import Iterable

from numpy import array
from fastapi import APIRouter


from ...utils import get_cg
from ...utils import string_array


router = APIRouter()


@router.get("/{graph_id}/change_log")
async def change_log_full(
    graph_id: str,
    start_time: Optional[float] = None,
    end_time: Optional[float] = None,
):
    """
    Returns a CSV file with operation details.
    Column Header: `operation_id, user_id, action, root_ids, timestamp`

    Use query parameters `start_time` and `end_time` to get operations in a given period.
    These can also be used individually.
    """
    from csv import writer
    from io import StringIO
    from datetime import datetime

    from pytz import UTC
    from fastapi.responses import Response

    from .logs_helpers import get_change_log

    si = StringIO()
    cw = writer(si)
    log_entries = get_change_log(
        graph_id,
        start_time=datetime.fromtimestamp(start_time, UTC) if start_time else None,
        end_time=datetime.fromtimestamp(end_time, UTC) if end_time else None,
    )

    cw.writerow(["operation_id", "user_id", "action", "root_ids", "timestamp"])
    cw.writerows(log_entries)
    output = si.getvalue()

    headers = {}
    headers["Content-Disposition"] = f"attachment; filename={graph_id}.csv"
    headers["Content-type"] = "text/csv"
    return Response(content=output, media_type="text/csv", headers=headers)


@router.get("/{graph_id}/operation_details")
async def operation_details(
    graph_id: str,
    operation_ids: Optional[str] = "[]",
):
    from json import loads
    from json import JSONDecodeError

    from pychunkedgraph.graph import exceptions

    from .logs_helpers import operation_details

    try:
        operation_ids = loads(operation_ids)
    except JSONDecodeError as e:
        raise exceptions.BadRequest(f"Operations IDs could not be parsed: {e}")
    return operation_details(graph_id, operation_ids)


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

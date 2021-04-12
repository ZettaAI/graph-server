"""
Various change log endpoints.
"""

from typing import Optional
from typing import Iterable

from fastapi import APIRouter
from pychunkedgraph.graph import segmenthistory

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

    from fastapi.responses import Response

    from .logs_helpers import get_change_log

    si = StringIO()
    cw = writer(si)
    log_entries = get_change_log(graph_id, start_time=start_time, end_time=end_time)

    cw.writerow(["operation_id", "user_id", "action", "root_ids", "timestamp"])
    cw.writerows(log_entries)
    output = si.getvalue()

    headers = {}
    headers["Content-Disposition"] = f"attachment; filename={graph_id}.csv"
    headers["Content-type"] = "text/csv"
    return Response(content=output, media_type="text/csv", headers=headers)


@router.get("/{graph_id}/root/{root_id}/change_log")
async def root_change_log(graph_id: str, root_id: int):
    return segmenthistory.SegmentHistory(get_cg(graph_id), int(root_id)).change_log()


@router.get("/{graph_id}/root/{root_id}/merge_log")
async def root_merge_log(graph_id: str, root_id: int):
    return segmenthistory.SegmentHistory(get_cg(graph_id), int(root_id)).merge_log()


@router.get("/{graph_id}/root/{root_id}/last_edit")
async def root_last_edit(graph_id: str, root_id: int, delimiter: Optional[str] = " "):
    ts = segmenthistory.SegmentHistory(
        get_cg(graph_id),
        int(root_id),
    ).last_edit.timestamp
    return {"iso": ts.isoformat(delimiter)}


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
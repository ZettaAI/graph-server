from typing import Optional

from fastapi import Request

from . import api
from . import get_cg
from .edits_helpers import format_edit_result


@api.post("/table/{graph_id}/merge")
async def merge(
    request: Request, graph_id: str, int64_as_str: Optional[bool] = False,
):
    from .edits_helpers import merge_helper

    return format_edit_result(merge_helper(get_cg(graph_id), request), int64_as_str)


@api.post("/table/{graph_id}/split")
async def split(
    request: Request, graph_id: str, int64_as_str: Optional[bool] = False,
):
    from .edits_helpers import split_helper

    return format_edit_result(split_helper(get_cg(graph_id), request), int64_as_str)


@api.post("/table/{graph_id}/graph/split_preview")
async def split_preview(
    request: Request, graph_id: str, int64_as_str: Optional[bool] = False,
):
    from .edits_helpers import split_preview_helper

    return split_preview_helper(get_cg(graph_id), request, int64_as_str=int64_as_str)


@api.post("/table/{graph_id}/undo")
async def undo(
    request: Request, graph_id: str, int64_as_str: Optional[bool] = False,
):
    from .edits_helpers import undo_helper

    return format_edit_result(undo_helper(get_cg(graph_id), request), int64_as_str)


@api.post("/table/{graph_id}/redo")
async def redo(
    request: Request, graph_id: str, int64_as_str: Optional[bool] = False,
):
    from .edits_helpers import redo_helper

    return format_edit_result(redo_helper(get_cg(graph_id), request), int64_as_str)

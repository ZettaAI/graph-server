from typing import Optional

from fastapi import Request
from fastapi import APIRouter

from .edits_helpers import format_edit_result
from ...utils import get_cg

router = APIRouter()


@router.post("/table/{graph_id}/merge")
async def merge(
    request: Request, graph_id: str, int64_as_str: Optional[bool] = False,
):
    from .edits_helpers import merge_helper

    return format_edit_result(
        await merge_helper(get_cg(graph_id), request), int64_as_str
    )


@router.post("/table/{graph_id}/split")
async def split(
    request: Request, graph_id: str, int64_as_str: Optional[bool] = False,
):
    from .edits_helpers import split_helper

    return format_edit_result(
        await split_helper(get_cg(graph_id), request), int64_as_str
    )


@router.post("/table/{graph_id}/graph/split_preview")
async def split_preview(
    request: Request, graph_id: str, int64_as_str: Optional[bool] = False,
):
    from .edits_helpers import split_preview_helper

    return await split_preview_helper(
        get_cg(graph_id), request, int64_as_str=int64_as_str
    )


@router.post("/table/{graph_id}/undo")
async def undo(
    request: Request, graph_id: str, int64_as_str: Optional[bool] = False,
):
    from .edits_helpers import undo_helper

    return format_edit_result(
        await undo_helper(get_cg(graph_id), request), int64_as_str
    )


@router.post("/table/{graph_id}/redo")
async def redo(
    request: Request, graph_id: str, int64_as_str: Optional[bool] = False,
):
    from .edits_helpers import redo_helper

    return format_edit_result(
        await redo_helper(get_cg(graph_id), request), int64_as_str
    )

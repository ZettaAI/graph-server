from typing import Optional
from copy import copy

from fastapi import Request
from fastapi import APIRouter
from pychunkedgraph.graph import exceptions

from .edits_helpers import format_edit_result
from ...utils import get_cg

router = APIRouter()


@router.post("/{graph_id}/merge")
async def merge(request: Request, graph_id: str, int64_as_str: Optional[bool] = False):
    from .edits_helpers import merge_helper

    try:
        result = await merge_helper(copy(get_cg(graph_id)), request)
    except exceptions.PreconditionError as e:
        raise exceptions.BadRequest(e)
    except exceptions.ChunkedGraphError as e:
        raise e
    except Exception as e:
        raise exceptions.InternalServerError(e)
    return format_edit_result(result, int64_as_str)


@router.post("/{graph_id}/split")
async def split(request: Request, graph_id: str, int64_as_str: Optional[bool] = False):
    from .edits_helpers import split_helper

    try:
        result = await split_helper(copy(get_cg(graph_id)), request)
    except exceptions.PreconditionError as e:
        raise exceptions.BadRequest(e)
    except exceptions.ChunkedGraphError as e:
        raise e
    except Exception as e:
        raise exceptions.InternalServerError(e)
    return format_edit_result(result, int64_as_str)


@router.post("/{graph_id}/graph/split_preview")
async def split_preview(
    request: Request, graph_id: str, int64_as_str: Optional[bool] = False
):
    from .edits_helpers import split_preview_helper

    try:
        return await split_preview_helper(
            copy(get_cg(graph_id)), request, int64_as_str=int64_as_str
        )
    except exceptions.PreconditionError as e:
        raise exceptions.BadRequest(e)
    except exceptions.ChunkedGraphError as e:
        raise e
    except Exception as e:
        raise exceptions.InternalServerError(e)


@router.post("/{graph_id}/undo")
async def undo(request: Request, graph_id: str, int64_as_str: Optional[bool] = False):
    from .edits_helpers import undo_helper

    try:
        result = await undo_helper(copy(get_cg(graph_id)), request)
    except exceptions.PreconditionError as e:
        raise exceptions.BadRequest(e)
    except exceptions.ChunkedGraphError as e:
        raise e
    except Exception as e:
        raise exceptions.InternalServerError(e)
    return format_edit_result(result, int64_as_str)


@router.post("/{graph_id}/redo")
async def redo(request: Request, graph_id: str, int64_as_str: Optional[bool] = False):
    from .edits_helpers import redo_helper

    try:
        result = await redo_helper(copy(get_cg(graph_id)), request)
    except exceptions.PreconditionError as e:
        raise exceptions.BadRequest(e)
    except exceptions.ChunkedGraphError as e:
        raise e
    except Exception as e:
        raise exceptions.InternalServerError(e)
    return format_edit_result(result, int64_as_str)

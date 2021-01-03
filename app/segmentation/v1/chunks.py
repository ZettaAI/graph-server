from typing import Optional
from datetime import datetime

from pytz import UTC
from fastapi import APIRouter

from ..utils import get_l2_chunk_children


router = APIRouter()


@router.get("/{graph_id}/l2_chunk_children/{chunk_id}")
async def l2_chunk_children(
    graph_id: str,
    chunk_id: int,
    timestamp: Optional[float] = None,
    int64_as_str: Optional[bool] = False,
    as_array: Optional[bool] = False,
):
    from pickle import dumps
    from ...utils import string_array

    children = get_l2_chunk_children(
        graph_id,
        chunk_id,
        timestamp=datetime.fromtimestamp(timestamp, UTC) if timestamp else None,
        flatten=as_array,
    )
    if as_array:
        if int64_as_str:
            return {"l2_chunk_children": string_array(children)}
        return {"l2_chunk_children": children.tolist()}
    return {"l2_chunk_children": dumps(children)}


@router.get("/{graph_id}/l2_chunk_children_binary/{chunk_id}")
async def l2_chunk_children_binary(
    graph_id: str,
    chunk_id: int,
    timestamp: Optional[float] = None,
    as_array: Optional[bool] = False,
):
    from pickle import dumps

    children = get_l2_chunk_children(
        graph_id,
        chunk_id,
        timestamp=datetime.fromtimestamp(timestamp, UTC) if timestamp else None,
        flatten=as_array,
    )
    if as_array:
        return children.tobytes()
    return dumps(children)

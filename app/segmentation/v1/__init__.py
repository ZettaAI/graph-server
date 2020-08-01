from typing import Optional
from typing import Iterable
import json
from time import time
from datetime import datetime

from pytz import UTC
from numpy import array
from numpy import uint64
from fastapi import Body
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from ...utils import get_cg
from ...utils import string_array

api = FastAPI()


@api.get("/table/{graph_id}/node/{node_id}/root")
async def root(
    graph_id: str,
    node_id: int,
    timestamp: Optional[float] = time(),
    stop_layer: Optional[int] = None,
    int64_as_str: Optional[bool] = True,
):
    timestamp = datetime.fromtimestamp(timestamp, UTC)
    root = get_cg(graph_id).get_root(
        node_id, stop_layer=stop_layer, time_stamp=timestamp
    )

    if int64_as_str:
        return {"root_id": str(root)}
    return {"root_id": root}


@api.post("/table/{graph_id}/roots")
async def roots(
    graph_id: str,
    node_ids: Iterable[int] = Body(...),
    stop_layer: Optional[int] = None,
    timestamp: Optional[float] = time(),
    int64_as_str: Optional[bool] = True,
):
    roots = get_cg(graph_id).get_roots(
        array(node_ids, dtype=uint64),
        stop_layer=stop_layer,
        time_stamp=datetime.fromtimestamp(timestamp, UTC),
    )

    if int64_as_str:
        return {"root_ids": string_array(roots)}
    return {"root_ids": roots}


@api.post("/table/{graph_id}/roots_binary")
async def roots_binary(
    request: Request,
    graph_id: str,
    node_id: int,
    stop_layer: Optional[int] = None,
    timestamp: Optional[float] = time(),
):
    from numpy import frombuffer

    timestamp = datetime.fromtimestamp(timestamp, UTC)
    node_ids = frombuffer(request.body, uint64)
    roots = get_cg(graph_id).get_roots(
        node_ids, stop_layer=stop_layer, time_stamp=timestamp
    )
    return roots.tobytes()


@api.post("/table/{graph_id}/node/{node_id}/children")
async def children(
    graph_id: str, node_id: int, int64_as_str: Optional[bool] = True,
):
    cg = get_cg(graph_id)
    node_id = uint64(node_id)
    children = array([], dtype=uint64)
    if cg.get_chunk_layer(node_id) > 1:
        children = cg.get_children(node_id)
    if int64_as_str:
        return {"root_ids": string_array(children)}
    return {"root_ids": children}

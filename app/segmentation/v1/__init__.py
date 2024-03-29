from typing import Optional
from typing import Iterable
from datetime import datetime

from pytz import UTC
from numpy import array
from numpy import uint64
from numpy import frombuffer
from fastapi import Body
from fastapi import FastAPI
from fastapi import Request

from .logs import router as logs_router
from .path import router as path_router
from .edits import router as edits_router
from .chunks import router as chunks_router
from .subgraph import router as subgraph_router
from .contact_sites import router as contact_sites_router

from ...utils import get_cg
from ...utils import string_array

api = FastAPI()
api.include_router(logs_router, prefix="/table")
api.include_router(path_router, prefix="/table")
api.include_router(edits_router, prefix="/table")
api.include_router(chunks_router, prefix="/table")
api.include_router(subgraph_router, prefix="/table")
api.include_router(contact_sites_router, prefix="/table")


@api.get("/table/{graph_id}/node/{node_id}/root")
async def root(
    graph_id: str,
    node_id: int,
    timestamp: Optional[float] = None,
    stop_layer: Optional[int] = None,
    int64_as_str: Optional[bool] = False,
):
    root = get_cg(graph_id).get_root(
        node_id,
        stop_layer=stop_layer,
        time_stamp=datetime.fromtimestamp(timestamp, UTC) if timestamp else None,
    )

    if int64_as_str:
        return {"root_id": str(root)}
    return {"root_id": int(root)}


@api.post("/table/{graph_id}/roots")
async def roots(
    graph_id: str,
    node_ids: Iterable[int] = Body(...),
    stop_layer: Optional[int] = None,
    timestamp: Optional[float] = None,
    int64_as_str: Optional[bool] = False,
):
    from numpy import fromiter

    roots = get_cg(graph_id).get_roots(
        fromiter(node_ids, dtype=uint64),
        stop_layer=stop_layer,
        time_stamp=datetime.fromtimestamp(timestamp, UTC) if timestamp else None,
    )

    if int64_as_str:
        return {"root_ids": string_array(roots)}
    return {"root_ids": roots.tolist()}


@api.post("/table/{graph_id}/roots_binary")
async def roots_binary(
    request: Request,
    graph_id: str,
    stop_layer: Optional[int] = None,
    timestamp: Optional[float] = None,
):
    from fastapi import Response

    node_ids = frombuffer(await request.body(), uint64)
    roots = get_cg(graph_id).get_roots(
        node_ids,
        stop_layer=stop_layer,
        time_stamp=datetime.fromtimestamp(timestamp, UTC) if timestamp else None,
    )
    return Response(content=roots.tobytes())


@api.post("/table/{graph_id}/is_latest_roots")
async def is_latest_roots(request: Request, graph_id: str):
    from json import loads

    from numpy import isin
    from pychunkedgraph.graph.attributes import Hierarchy

    node_ids = frombuffer(await request.body(), uint64)
    rows_d = get_cg(graph_id).client.read_nodes(
        node_ids=node_ids, columns=Hierarchy.NewParent
    )
    return ~isin(node_ids, list(rows_d.keys()))


@api.get("/table/{graph_id}/node/{node_id}/children")
async def children(
    graph_id: str,
    node_id: int,
    int64_as_str: Optional[bool] = False,
):
    cg = get_cg(graph_id)
    node_id = uint64(node_id)
    children = array([], dtype=uint64)
    if cg.get_chunk_layer(node_id) > 1:
        children = cg.get_children(node_id)
    if int64_as_str:
        return {"root_ids": string_array(children)}
    return {"root_ids": children.tolist()}

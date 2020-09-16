from typing import Optional
from json import loads

from numpy import array
from numpy import uint64
from fastapi import FastAPI
from fastapi import Request

from ..utils import get_cg

api = FastAPI()


@api.get("/table/{graph_id}/manifest/{node_id}:0")
async def manifest(
    request: Request,
    graph_id: str,
    node_id: int,
    verify: Optional[bool] = True,
    return_seg_ids: Optional[bool] = False,
    prepend_seg_ids: Optional[bool] = False,
    bounds: Optional[str] = "",
):
    from json.decoder import JSONDecodeError
    from .utils import manifest_response

    try:
        data = loads(await request.body())
    except JSONDecodeError:
        data = {}
    bbox = None
    if bounds:
        bbox = array([b.split("-") for b in bounds.split("_")], dtype=int).T

    cg = get_cg(graph_id)
    start_layer = cg.meta.custom_data.get("mesh", {}).get("max_layer", 2)
    if "start_layer" in data:
        start_layer = int(data["start_layer"])

    flexible_start_layer = None
    if "flexible_start_layer" in data:
        flexible_start_layer = int(data["flexible_start_layer"])

    args = (
        node_id,
        verify,
        return_seg_ids,
        prepend_seg_ids,
        start_layer,
        flexible_start_layer,
        bbox,
        data,
    )
    return manifest_response(cg, args)


@api.post("/table/{graph_id}/remesh")
async def remesh(request: Request, graph_id: str):
    from .utils import remesh

    data = loads(await request.body())
    return remesh(
        get_cg(graph_id), data["operation_id"], array(data["l2ids"], dtype=uint64)
    )

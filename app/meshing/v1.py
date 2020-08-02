from typing import Optional

from fastapi import FastAPI
from fastapi import Request

api = FastAPI()


@api.get("/table/{graph_id}/manifest/{node_id}:0")
async def manifest(
    request: Request,
    graph_id: str,
    node_id: int,
    verify: Optional[bool] = True,
    return_seg_ids: Optional[bool] = True,
    prepend_seg_ids: Optional[bool] = True,
    bounds: Optional[str] = "",
):
    from json import loads
    from numpy import array
    from numpy import uint64
    from .utils import manifest_response
    from ..utils import get_cg

    data = {}
    if len(request.body) > 0:
        data = loads(request.data)

    bbox = None
    if bounds:
        bbox = array([b.split("-") for b in bounds.split("_")], dtype=int).T

    cg = get_cg(graph_id)
    start_layer = cg.get_chunk_layer(uint64(node_id))
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


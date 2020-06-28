from json import dumps

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from ..utils import get_info

api = FastAPI()


@api.get("/table/{graph_id}/node/{node_id}/root")
async def root(graph_id: str, node_id: int, int64_as_str: bool):
    from .graph import get_root

    return {"root_id": str(await get_root(graph_id, node_id))}


@api.get("/table/{graph_id}/node/{node_id}/leaves")
async def leaves(graph_id: str, node_id: int, int64_as_str: bool, bounds: str):
    from .graph import get_leaves

    return {"leaf_ids": [str(x) for x in await get_leaves(graph_id, node_id, bounds)]}

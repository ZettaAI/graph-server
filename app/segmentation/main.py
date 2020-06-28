from json import dumps

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from ..utils import get_info

api = FastAPI()


@api.get("/table/{graph_id}/info")
async def handle_info(graph_id: str):
    return await get_info(graph_id)

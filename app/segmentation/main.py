from fastapi import FastAPI

api = FastAPI()


@api.get("")
@api.get("/")
async def home(graph_id: str):
    from pychunkedgraph import __version__

    return f"Segmentation API: ChunkedGraph Version {__version__}"


@api.get("/table/{graph_id}/info")
async def info(graph_id: str):
    from ..utils import get_info

    return await get_info(graph_id)

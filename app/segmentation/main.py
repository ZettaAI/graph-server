from fastapi import FastAPI

api = FastAPI()


@api.get("")
@api.get("/")
async def home():
    from pychunkedgraph import __version__

    return {"version": f"ChunkedGraph Segmentation API {__version__}"}


@api.get("/table/{graph_id}/info")
async def info(graph_id: str):
    from pychunkedgraph.graph.exceptions import InternalServerError
    from ..utils import get_info

    try:
        return await get_info(graph_id)
    except Exception as e:
        raise InternalServerError(e)

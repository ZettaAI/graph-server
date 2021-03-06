from fastapi import FastAPI

api = FastAPI()


@api.get("")
@api.get("/")
async def home():
    from pychunkedgraph import __version__

    return {"version": f"ChunkedGraph Meshing API {__version__}"}

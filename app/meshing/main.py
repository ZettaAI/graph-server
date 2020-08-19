from fastapi import FastAPI

api = FastAPI()


@api.get("")
@api.get("/")
async def home():
    from pychunkedgraph import __version__

    return f"Meshing API: ChunkedGraph Version {__version__}"

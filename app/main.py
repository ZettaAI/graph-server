from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .middleware import ResponseTimeHeader
from .meshing import api as meshing_api
from .segmentation import api as segmentation_api


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ResponseTimeHeader)

app.mount("/meshing", meshing_api)
app.mount("/segmentation", segmentation_api)


@app.on_event("startup")
async def startup_event():
    from .utils import preload_datasets

    preload_datasets()


@app.get("/")
async def home():
    from . import __version__

    return {"version": f"Graph Server {__version__}"}

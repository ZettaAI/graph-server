from time import time

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .utils import get_cg
from .utils import get_info
from .middleware import ResponseTimeHeader
from .segmentation import api as segmentation_api


# TODO add tests and configure CI/CD
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ResponseTimeHeader)


app.mount("/segmentation", segmentation_api)

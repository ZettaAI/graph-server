from .main import api
from .v1 import api as v1_api


api.mount("/api/v1", v1_api)

from time import time

from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware


class ResponseTimeHeader(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time()
        response = await call_next(request)
        response.headers["X-Process-Time"] = str(time() - start_time)
        return response

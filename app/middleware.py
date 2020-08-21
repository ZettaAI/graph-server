from time import time

from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # TODO auth middleware here or traefik?
        response = await call_next(request)
        return response


class ResponseTimeHeader(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time()
        response = await call_next(request)
        response.headers["X-Process-Time"] = str(time() - start_time)
        return response


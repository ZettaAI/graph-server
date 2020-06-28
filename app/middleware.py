from time import time

from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # TODO add auth logic
        response = await call_next(request)
        return response


class ResponseTimeHeader(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time()
        response = await call_next(request)
        process_time = time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response


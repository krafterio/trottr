from starlette.middleware.base import BaseHTTPMiddleware
from core.context import set_request, reset_request


class ContextRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        token = set_request(request)

        try:
            return await call_next(request)
        finally:
            reset_request(token)

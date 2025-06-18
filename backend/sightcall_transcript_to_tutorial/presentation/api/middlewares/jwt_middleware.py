from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED

from sightcall_transcript_to_tutorial.domain.config.settings import settings

PUBLIC_ENDPOINTS = ["/auth/github/login", "/auth/github/callback", "/docs", "/openapi.json"]


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow OPTIONS requests (CORS preflight) to pass through without authentication
        if request.method == "OPTIONS":
            return await call_next(request)

        # Allow public endpoints without JWT
        if any(map(request.url.path.startswith, PUBLIC_ENDPOINTS)) or request.url.path == "/":
            return await call_next(request)

        # Try to get token from Authorization header first (for API calls)
        token = self._extract_token_from_header(request)

        # If no header token, try to get from cookie (for browser requests)
        if not token:
            token = self._extract_token_from_cookie(request)

        if not token:
            return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED, content={"detail": "Missing or invalid authentication token"}
            )

        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
            request.state.user = payload  # Attach user info to request.state
        except Exception as e:
            return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content={"detail": f"Invalid token: {repr(e)}"})

        return await call_next(request)

    def _extract_token_from_header(self, request: Request) -> str | None:
        """Extract JWT token from Authorization header"""
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        return auth_header.split(" ", 1)[1]

    def _extract_token_from_cookie(self, request: Request) -> str | None:
        """Extract JWT token from HttpOnly cookie"""
        return request.cookies.get("access_token")

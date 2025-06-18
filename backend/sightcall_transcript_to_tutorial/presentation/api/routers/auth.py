from http import HTTPStatus
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from sightcall_transcript_to_tutorial.application.commands.login_command import LoginCommand
from sightcall_transcript_to_tutorial.application.queries.get_authenticated_user_query import GetAuthenticatedUserQuery
from sightcall_transcript_to_tutorial.domain.config import settings
from sightcall_transcript_to_tutorial.infrastructure.for_production.gateways.github_authentication_gateway import (
    GitHubAuthenticationGateway,
    GitHubOAuthError,
)
from sightcall_transcript_to_tutorial.infrastructure.for_production.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from sightcall_transcript_to_tutorial.presentation.api.dependencies import get_session
from sightcall_transcript_to_tutorial.presentation.api.schemas.auth import AuthResponseSchema

router = APIRouter(prefix="/auth/github", tags=["auth"])

# Constants
JWT_COOKIE_NAME = "access_token"
JWT_COOKIE_MAX_AGE_SECONDS = 3600
COOKIE_PATH = "/"


@router.get("/login")
def github_login(db: Session = Depends(get_session)):
    login_url = _execute_login_command(db)
    return {"login_url": login_url}


@router.get("/callback", response_model=AuthResponseSchema)
def github_callback(code: str = Query(...), db: Session = Depends(get_session)):
    jwt_token = _authenticate_user_with_code(code, db)
    response = _create_redirect_response()
    _set_jwt_cookie(response, jwt_token)
    return response


@router.get("/me")
def get_current_user(request: Request):
    user_payload = _extract_user_payload_from_request(request)
    user_info = _build_user_info_from_payload(user_payload)
    return user_info


@router.post("/logout")
def logout():
    response = _create_logout_redirect_response()
    _clear_jwt_cookie(response)
    return response


def _execute_login_command(db: Session) -> str:
    """Execute the login command to get GitHub OAuth URL."""
    user_repo = SQLAlchemyUserRepository(db)
    gateway = GitHubAuthenticationGateway(user_repo)
    command = LoginCommand(gateway)
    return command.execute()


def _authenticate_user_with_code(code: str, db: Session) -> str:
    """Authenticate user with OAuth code and return JWT token."""
    user_repo = SQLAlchemyUserRepository(db)
    gateway = GitHubAuthenticationGateway(user_repo)
    query = GetAuthenticatedUserQuery(gateway, user_repo)

    try:
        _, jwt_token = query.execute(code)
        return jwt_token
    except GitHubOAuthError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=repr(e))
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=repr(e))


def _create_redirect_response() -> RedirectResponse:
    """Create redirect response to frontend callback success page."""
    return RedirectResponse(url=f"{settings.frontend_url}/auth/callback/success")


def _set_jwt_cookie(response: RedirectResponse, jwt_token: str) -> None:
    """Set JWT token in secure HTTP-only cookie."""
    response.set_cookie(
        key=JWT_COOKIE_NAME,
        value=jwt_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=JWT_COOKIE_MAX_AGE_SECONDS,
        path=COOKIE_PATH,
    )


def _extract_user_payload_from_request(request: Request) -> Dict[str, Any]:
    """Extract user payload from request state."""
    payload = getattr(request.state, "user", None)
    if not payload:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Not authenticated")
    return payload


def _build_user_info_from_payload(payload: Dict[str, Any]) -> Dict[str, str]:
    """Build user info response from JWT payload."""
    user_id = payload.get("user_id")
    name = payload.get("username")

    if not user_id or not name:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token payload")

    return {"id": user_id, "name": name}


def _create_logout_redirect_response() -> RedirectResponse:
    """Create redirect response for logout."""
    return RedirectResponse(url=f"{settings.frontend_url}", status_code=HTTPStatus.SEE_OTHER)


def _clear_jwt_cookie(response: RedirectResponse) -> None:
    """Clear JWT cookie on logout."""
    response.delete_cookie(key=JWT_COOKIE_NAME, path=COOKIE_PATH, httponly=True, secure=True, samesite="lax")

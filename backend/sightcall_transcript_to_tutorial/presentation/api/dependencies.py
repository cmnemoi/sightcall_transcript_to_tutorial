from http import HTTPStatus
from typing import Any, Dict, Generator

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from sightcall_transcript_to_tutorial.domain.entities.user import User
from sightcall_transcript_to_tutorial.domain.gateways.authentication_gateway_interface import (
    AuthenticationGatewayInterface,
)
from sightcall_transcript_to_tutorial.domain.gateways.tutorial_generator_gateway_interface import (
    TutorialGeneratorGatewayInterface,
)
from sightcall_transcript_to_tutorial.domain.repositories.transcript_repository_interface import (
    TranscriptRepositoryInterface,
)
from sightcall_transcript_to_tutorial.domain.repositories.tutorial_repository_interface import (
    TutorialRepositoryInterface,
)
from sightcall_transcript_to_tutorial.domain.repositories.user_repository_interface import UserRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId
from sightcall_transcript_to_tutorial.infrastructure.for_production.gateways.github_authentication_gateway import (
    GitHubAuthenticationGateway,
)
from sightcall_transcript_to_tutorial.infrastructure.for_production.gateways.openai_tutorial_generator_gateway import (
    OpenAITutorialGeneratorGateway,
)
from sightcall_transcript_to_tutorial.infrastructure.for_production.models.base import SessionLocal
from sightcall_transcript_to_tutorial.infrastructure.for_production.repositories.sqlalchemy_transcript_repository import (
    SQLAlchemyTranscriptRepository,
)
from sightcall_transcript_to_tutorial.infrastructure.for_production.repositories.sqlalchemy_tutorial_repository import (
    SQLAlchemyTutorialRepository,
)
from sightcall_transcript_to_tutorial.infrastructure.for_production.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)

security = HTTPBearer()


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_transcript_repository(session: Session = Depends(get_session)) -> TranscriptRepositoryInterface:
    return SQLAlchemyTranscriptRepository(session)


def get_tutorial_generator_gateway() -> TutorialGeneratorGatewayInterface:
    return OpenAITutorialGeneratorGateway()


def get_tutorial_repository(session: Session = Depends(get_session)) -> TutorialRepositoryInterface:
    return SQLAlchemyTutorialRepository(session)


def get_authentication_gateway(user_repository: UserRepositoryInterface) -> AuthenticationGatewayInterface:
    return GitHubAuthenticationGateway(user_repository)


def get_user_repository(session: Session = Depends(get_session)) -> UserRepositoryInterface:
    return SQLAlchemyUserRepository(session)


def get_current_user_from_request_state(
    request: Request, user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> User:
    """
    Extract user from request state (set by JWT middleware from cookie).
    This replaces the HTTPBearer dependency for cookie-based authentication.
    """
    user_payload = _extract_user_payload_from_request(request)
    return _build_user_from_payload(user_payload, user_repository)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repository=Depends(get_user_repository),
) -> User:
    authentication_gateway = get_authentication_gateway(user_repository)
    try:
        return authentication_gateway.get_current_user_from_jwt(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED.value, detail="Invalid token")


def _extract_user_payload_from_request(request: Request) -> Dict[str, Any]:
    """Extract user payload from request state."""
    payload = getattr(request.state, "user", None)
    if not payload:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED.value, detail="Not authenticated")
    return payload


def _build_user_from_payload(payload: Dict[str, Any], user_repository: UserRepositoryInterface) -> User:
    """Build User entity from JWT payload."""
    user_id = payload.get("user_id")
    name = payload.get("username")

    if not user_id or not name:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED.value, detail="Invalid token payload")

    user = user_repository.find_by_id(UserId(user_id))
    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED.value, detail="Invalid token payload")
    return user

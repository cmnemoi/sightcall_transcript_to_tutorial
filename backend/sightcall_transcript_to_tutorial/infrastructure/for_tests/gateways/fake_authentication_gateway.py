from sightcall_transcript_to_tutorial.domain.entities.authenticated_user import AuthenticatedUser
from sightcall_transcript_to_tutorial.domain.entities.user import User
from sightcall_transcript_to_tutorial.domain.gateways.authentication_gateway_interface import (
    AuthenticationGatewayInterface,
)
from sightcall_transcript_to_tutorial.domain.repositories.user_repository_interface import UserRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId


class FakeAuthenticationGateway(AuthenticationGatewayInterface):
    _FAKE_USER = AuthenticatedUser(1, "fakeuser", "fake@user.com")
    _VALID_CODE = "valid_code"
    _VALID_TOKEN = "valid_token"

    def __init__(self, user_repository: UserRepositoryInterface):
        self._user_repository = user_repository

    def get_login_url(self) -> str:
        return "https://fake-oauth/login"

    def authenticate_callback(self, code: str) -> AuthenticatedUser:
        if code == self._VALID_CODE:
            return self._FAKE_USER
        raise ValueError("Invalid code")

    def create_jwt(self, user: User) -> str:
        # Accept both User and AuthenticatedUser for test compatibility
        if hasattr(user, "user_id"):
            user_id = user.user_id.value
        else:
            # For AuthenticatedUser, synthesize a fake user_id for legacy tests
            user_id = "fake-user-id"
        github_id = user.github_id
        payload = {"user_id": user_id, "github_id": github_id}
        self._last_payload = payload  # For test inspection
        return f"jwt:{payload['user_id']}:{payload['github_id']}"

    def verify_jwt(self, token: str) -> AuthenticatedUser:
        if token == self._VALID_TOKEN:
            return self._FAKE_USER
        raise ValueError("Invalid token")

    def get_current_user_from_jwt(self, token: str) -> User:
        # Simulate decoding the JWT
        if not token.startswith("jwt:"):
            payload = getattr(self, "_last_payload", None)
            if not payload:
                raise ValueError("Invalid token")
        else:
            try:
                _, user_id, github_id = token.split(":")
                payload = {"user_id": user_id, "github_id": int(github_id)}
            except Exception:
                raise ValueError("Malformed token")
        if "user_id" not in payload or not payload["user_id"]:
            raise ValueError("JWT missing user_id")
        if "github_id" not in payload or payload["github_id"] is None:
            raise ValueError("JWT missing github_id")
        user = self._user_repository.find_by_id(UserId(payload["user_id"]))
        if not user:
            raise ValueError("User not found")
        if user.github_id != payload["github_id"]:
            raise ValueError("github_id mismatch")
        return user

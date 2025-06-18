from abc import ABC, abstractmethod

from sightcall_transcript_to_tutorial.domain.entities.authenticated_user import AuthenticatedUser
from sightcall_transcript_to_tutorial.domain.entities.user import User


class AuthenticationGatewayInterface(ABC):
    @abstractmethod
    def get_login_url(self) -> str:
        pass

    @abstractmethod
    def authenticate_callback(self, code: str) -> AuthenticatedUser:
        pass

    @abstractmethod
    def create_jwt(self, user: User) -> str:
        pass

    @abstractmethod
    def verify_jwt(self, token: str) -> AuthenticatedUser:
        pass

    @abstractmethod
    def get_current_user_from_jwt(self, token: str) -> User:
        """
        Extracts a User from a JWT token using the user repository (provided at construction).
        JWT must contain both user_id and github_id.
        Raises ValueError if invalid or user not found.
        """
        pass

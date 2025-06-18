from sightcall_transcript_to_tutorial.domain.entities.user import User
from sightcall_transcript_to_tutorial.domain.gateways.authentication_gateway_interface import (
    AuthenticationGatewayInterface,
)
from sightcall_transcript_to_tutorial.domain.repositories.user_repository_interface import UserRepositoryInterface


class GetAuthenticatedUserQuery:
    def __init__(self, gateway: AuthenticationGatewayInterface, user_repo: UserRepositoryInterface):
        self.gateway = gateway
        self.user_repo = user_repo

    def execute(self, code: str) -> tuple[User, str]:
        auth_user = self.gateway.authenticate_callback(code)
        user = self.user_repo.find_by_github_id(auth_user.github_id)
        if not user:
            user = User.from_authenticated_user(auth_user)
            self.user_repo.save(user)
        jwt = self.gateway.create_jwt(user)
        return user, jwt

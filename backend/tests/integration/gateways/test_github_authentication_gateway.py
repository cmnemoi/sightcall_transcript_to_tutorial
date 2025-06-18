from jose import jwt

from sightcall_transcript_to_tutorial.domain.config.settings import settings
from sightcall_transcript_to_tutorial.domain.entities.user import User
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId
from sightcall_transcript_to_tutorial.infrastructure.for_production.gateways.github_authentication_gateway import (
    GitHubAuthenticationGateway,
)
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_user_repository import (
    FakeUserRepository,
)


class TestGitHubAuthenticationGatewayJWTCreation:
    """Test JWT creation functionality of GitHubAuthenticationGateway"""

    def test_should_create_jwt_with_required_payload_fields(self):
        """Test that JWT contains all required fields for authentication"""
        # Given
        user_repo, gateway, test_user = self._given_gateway_with_test_user()

        # When
        jwt_token = self._when_creating_jwt_for_user(gateway, test_user)

        # Then
        self._then_jwt_should_contain_required_fields(jwt_token, test_user)

    def test_should_create_jwt_with_current_payload_structure_for_me_endpoint(self):
        """Test JWT payload structure compatibility with /me endpoint expectations"""
        # Given
        user_repo, gateway, test_user = self._given_gateway_with_test_user()

        # When
        jwt_token = self._when_creating_jwt_for_user(gateway, test_user)

        # Then
        self._then_jwt_should_have_me_endpoint_compatible_structure(jwt_token, test_user)

    def test_should_create_jwt_maintaining_backward_compatibility(self):
        """Test that JWT maintains backward compatibility for internal gateway methods"""
        # Given
        user_repo, gateway, test_user = self._given_gateway_with_test_user()

        # When
        jwt_token = self._when_creating_jwt_for_user(gateway, test_user)

        # Then
        self._then_jwt_should_maintain_backward_compatibility_fields(jwt_token, test_user)

    def _given_gateway_with_test_user(self):
        """Setup test dependencies and create test user"""
        user_repo = FakeUserRepository()
        gateway = GitHubAuthenticationGateway(user_repo)
        test_user = User(user_id=UserId("user-123"), name="testuser", github_id=42)
        return user_repo, gateway, test_user

    def _when_creating_jwt_for_user(self, gateway: GitHubAuthenticationGateway, user: User) -> str:
        """Execute JWT creation for the given user"""
        return gateway.create_jwt(user)

    def _then_jwt_should_contain_required_fields(self, jwt_token: str, expected_user: User) -> None:
        """Verify JWT contains all required authentication fields"""
        payload = jwt.decode(jwt_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])

        assert "user_id" in payload, "JWT should contain 'user_id' field"
        assert "github_id" in payload, "JWT should contain 'github_id' field"
        assert "username" in payload, "JWT should contain 'username' field"

        assert payload["user_id"] == expected_user.user_id.value
        assert payload["github_id"] == expected_user.github_id
        assert payload["username"] == expected_user.name

    def _then_jwt_should_have_me_endpoint_compatible_structure(self, jwt_token: str, expected_user: User) -> None:
        """Verify JWT structure is compatible with /me endpoint expectations"""
        payload = jwt.decode(jwt_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])

        # Current /me endpoint expects these specific fields
        assert "user_id" in payload, "JWT should contain 'user_id' field for /me endpoint"
        assert "username" in payload, "JWT should contain 'username' field for /me endpoint"

        assert payload["user_id"] == expected_user.user_id.value
        assert payload["username"] == expected_user.name

    def _then_jwt_should_maintain_backward_compatibility_fields(self, jwt_token: str, expected_user: User) -> None:
        """Verify JWT maintains fields required for internal gateway methods"""
        payload = jwt.decode(jwt_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])

        # Internal methods require these fields
        assert "user_id" in payload, "JWT should contain 'user_id' for internal compatibility"
        assert "github_id" in payload, "JWT should contain 'github_id' for internal compatibility"

        assert payload["user_id"] == expected_user.user_id.value
        assert payload["github_id"] == expected_user.github_id

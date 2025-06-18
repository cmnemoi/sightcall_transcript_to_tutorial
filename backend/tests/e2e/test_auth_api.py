from http import HTTPStatus

from fastapi.testclient import TestClient
from jose import jwt

from sightcall_transcript_to_tutorial.domain.config.settings import settings
from sightcall_transcript_to_tutorial.domain.entities.user import User
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_user_repository import (
    FakeUserRepository,
)
from sightcall_transcript_to_tutorial.main import app
from sightcall_transcript_to_tutorial.presentation.api.dependencies import get_user_repository

client = TestClient(app)

# Test constants
TEST_USER_ID = "test-user-123"
TEST_GITHUB_ID = 42
TEST_USERNAME = "testuser"


class TestAuthMeEndpoint:
    """Test /auth/github/me endpoint authentication functionality"""

    def test_should_return_user_info_when_authenticated_with_valid_jwt(self):
        """Test successful user info retrieval with valid JWT token"""
        # Given
        self._given_test_user_repository_with_user()
        auth_cookies = self._given_valid_auth_cookies()

        try:
            # When
            response = self._when_calling_me_endpoint_with_cookies(auth_cookies)

            # Then
            self._then_should_return_successful_user_info(response)
        finally:
            self._cleanup_dependency_overrides()

    def test_should_return_unauthorized_when_jwt_missing_required_fields(self):
        """Test authentication failure when JWT lacks required fields"""
        # Given
        self._given_test_user_repository_with_user()
        incomplete_cookies = self._given_incomplete_jwt_cookies()

        try:
            # When
            response = self._when_calling_me_endpoint_with_cookies(incomplete_cookies)

            # Then
            self._then_should_return_unauthorized_for_invalid_token(response)
        finally:
            self._cleanup_dependency_overrides()

    def _given_test_user_repository_with_user(self) -> None:
        """Setup test user repository with a test user"""
        app.dependency_overrides[get_user_repository] = self._create_test_user_repository

    def _given_valid_auth_cookies(self) -> dict[str, str]:
        """Create valid authentication cookies with complete JWT payload"""
        return self._create_auth_cookies(user_id=TEST_USER_ID, github_id=TEST_GITHUB_ID, username=TEST_USERNAME)

    def _given_incomplete_jwt_cookies(self) -> dict[str, str]:
        """Create cookies with incomplete JWT payload missing required fields"""
        incomplete_payload = {"github_id": TEST_GITHUB_ID}  # Missing user_id and username
        token = jwt.encode(incomplete_payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return {"access_token": token}

    def _when_calling_me_endpoint_with_cookies(self, cookies: dict[str, str]):
        """Execute call to /me endpoint with provided cookies"""
        return client.get("/auth/github/me", cookies=cookies)

    def _then_should_return_successful_user_info(self, response) -> None:
        """Verify successful response with correct user information"""
        assert response.status_code == HTTPStatus.OK
        user_data = response.json()
        assert user_data["id"] == TEST_USER_ID
        assert user_data["name"] == TEST_USERNAME

    def _then_should_return_unauthorized_for_invalid_token(self, response) -> None:
        """Verify unauthorized response for invalid token"""
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        error_detail = response.json()["detail"]
        assert "Invalid token payload" in error_detail

    def _create_test_user_repository(self) -> FakeUserRepository:
        """Create test user repository with pre-populated test user"""
        user_repo = FakeUserRepository()
        test_user = User(user_id=UserId(TEST_USER_ID), name=TEST_USERNAME, github_id=TEST_GITHUB_ID)
        user_repo.save(test_user)
        return user_repo

    def _create_auth_cookies(
        self, user_id: str = TEST_USER_ID, github_id: int = TEST_GITHUB_ID, username: str = TEST_USERNAME
    ) -> dict[str, str]:
        """Create authentication cookies with JWT token"""
        payload = {"user_id": user_id, "github_id": github_id, "username": username}
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return {"access_token": token}

    def _cleanup_dependency_overrides(self) -> None:
        """Clean up dependency overrides after test"""
        app.dependency_overrides.clear()


class TestAuthLoginEndpoint:
    """Test /auth/github/login endpoint functionality"""

    def test_should_return_github_oauth_login_url(self):
        """Test that login endpoint returns valid GitHub OAuth URL"""
        # Given - No setup required for login endpoint

        # When
        response = self._when_calling_login_endpoint()

        # Then
        self._then_should_return_github_oauth_url(response)

    def _when_calling_login_endpoint(self):
        """Execute call to login endpoint"""
        return client.get("/auth/github/login")

    def _then_should_return_github_oauth_url(self, response) -> None:
        """Verify response contains valid GitHub OAuth URL"""
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()
        assert "login_url" in response_data
        assert "https://github.com/login/oauth/authorize" in response_data["login_url"]

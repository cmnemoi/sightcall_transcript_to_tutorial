import pytest

from sightcall_transcript_to_tutorial.application.queries.get_authenticated_user_query import GetAuthenticatedUserQuery
from sightcall_transcript_to_tutorial.domain.entities.user import User
from sightcall_transcript_to_tutorial.domain.value_objects import UserId
from sightcall_transcript_to_tutorial.infrastructure.for_tests.gateways.fake_authentication_gateway import (
    FakeAuthenticationGateway,
)
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_user_repository import (
    FakeUserRepository,
)


class TestGetAuthenticatedUserQuery:
    """Test GetAuthenticatedUserQuery for user authentication and JWT generation"""

    def test_should_create_new_user_and_return_jwt_when_user_does_not_exist(self):
        """Test successful creation of new user and JWT generation"""
        # Given
        user_repo, gateway, query = self._given_query_with_empty_repository()

        # When
        user, jwt_token = self._when_executing_query_with_valid_code(query)

        # Then
        self._then_should_create_and_persist_new_user(user, user_repo)
        self._then_should_return_valid_jwt_token(jwt_token, user)

    def test_should_return_existing_user_and_jwt_when_user_already_exists(self):
        """Test retrieval of existing user and JWT generation"""
        # Given
        user_repo, gateway, query, existing_user = self._given_query_with_existing_user()

        # When
        returned_user, jwt_token = self._when_executing_query_with_valid_code(query)

        # Then
        self._then_should_return_existing_user(returned_user, existing_user)
        self._then_should_return_valid_jwt_token(jwt_token, returned_user)

    def test_should_raise_error_when_authentication_code_is_invalid(self):
        """Test error handling for invalid authentication code"""
        # Given
        user_repo, gateway, query = self._given_query_with_empty_repository()

        # When & Then
        with pytest.raises(ValueError):
            self._when_executing_query_with_invalid_code(query)

    def _given_query_with_empty_repository(self):
        """Setup query with empty user repository"""
        user_repo = FakeUserRepository()
        gateway = FakeAuthenticationGateway(user_repo)
        query = GetAuthenticatedUserQuery(gateway, user_repo)
        return user_repo, gateway, query

    def _given_query_with_existing_user(self):
        """Setup query with existing user in repository"""
        user_repo = FakeUserRepository()
        gateway = FakeAuthenticationGateway(user_repo)
        existing_user = User(user_id=UserId.generate(), name="octocat", github_id=1)
        user_repo.save(existing_user)
        query = GetAuthenticatedUserQuery(gateway, user_repo)
        return user_repo, gateway, query, existing_user

    def _when_executing_query_with_valid_code(self, query: GetAuthenticatedUserQuery):
        """Execute query with valid authentication code"""
        return query.execute("valid_code")

    def _when_executing_query_with_invalid_code(self, query: GetAuthenticatedUserQuery):
        """Execute query with invalid authentication code"""
        return query.execute("invalid_code")

    def _then_should_create_and_persist_new_user(self, user: User, user_repo: FakeUserRepository) -> None:
        """Verify that new user was created and persisted"""
        assert isinstance(user, User)

        persisted_user = user_repo.find_by_github_id(1)
        assert persisted_user is not None
        assert persisted_user.github_id == 1

    def _then_should_return_existing_user(self, returned_user: User, expected_user: User) -> None:
        """Verify that existing user was returned"""
        assert returned_user.user_id == expected_user.user_id
        assert returned_user.github_id == expected_user.github_id

    def _then_should_return_valid_jwt_token(self, jwt_token: str, user: User) -> None:
        """Verify that valid JWT token was returned"""
        assert isinstance(jwt_token, str)
        expected_jwt = f"jwt:{user.user_id.value}:{user.github_id}"
        assert jwt_token == expected_jwt

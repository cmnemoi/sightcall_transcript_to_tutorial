# TDD: Tests for FakeAuthenticationGateway (in-memory, for unit tests)
import pytest

from sightcall_transcript_to_tutorial.domain.entities.authenticated_user import AuthenticatedUser
from sightcall_transcript_to_tutorial.domain.entities.user import User
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId
from sightcall_transcript_to_tutorial.infrastructure.for_tests.gateways.fake_authentication_gateway import (
    FakeAuthenticationGateway,
)
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_user_repository import (
    FakeUserRepository,
)


class TestFakeAuthenticationGateway:
    def test_should_return_fixed_login_url(self):
        user_repo = FakeUserRepository()
        gateway = FakeAuthenticationGateway(user_repo)
        assert gateway.get_login_url() == "https://fake-oauth/login"

    def test_should_authenticate_known_code(self):
        user_repo = FakeUserRepository()
        gateway = FakeAuthenticationGateway(user_repo)
        user = gateway.authenticate_callback("valid_code")
        assert isinstance(user, AuthenticatedUser)
        assert user.github_id == 1
        assert user.username == "fakeuser"
        assert user.email == "fake@user.com"

    def test_should_raise_on_unknown_code(self):
        user_repo = FakeUserRepository()
        gateway = FakeAuthenticationGateway(user_repo)
        with pytest.raises(ValueError):
            gateway.authenticate_callback("invalid_code")

    def test_should_create_and_verify_jwt(self):
        user_repo = FakeUserRepository()
        gateway = FakeAuthenticationGateway(user_repo)
        user = User(user_id=UserId("user-123"), name="fakeuser", github_id=1)
        token = gateway.create_jwt(user)
        # Simulate JWT verification by decoding the token
        # (for fake, just check the format and values)
        assert token == f"jwt:{user.user_id.value}:{user.github_id}"

    def test_should_raise_on_invalid_jwt(self):
        user_repo = FakeUserRepository()
        gateway = FakeAuthenticationGateway(user_repo)
        with pytest.raises(ValueError):
            gateway.verify_jwt("bad_token")

    def test_should_extract_user_from_jwt(self):
        user_repo = FakeUserRepository()
        gateway = FakeAuthenticationGateway(user_repo)
        user = User(user_id=UserId("user-123"), name="fakeuser", github_id=1)
        user_repo.save(user)
        token = gateway.create_jwt(user)
        extracted = gateway.get_current_user_from_jwt(token)
        assert extracted == user

    def test_should_raise_on_invalid_jwt_for_user_extraction(self):
        user_repo = FakeUserRepository()
        gateway = FakeAuthenticationGateway(user_repo)
        with pytest.raises(ValueError):
            gateway.get_current_user_from_jwt("bad_token")

    def test_should_raise_if_user_id_missing_in_jwt(self):
        user_repo = FakeUserRepository()
        gateway = FakeAuthenticationGateway(user_repo)
        token = "token_missing_user_id"
        gateway._last_payload = {"github_id": 1}
        with pytest.raises(ValueError):
            gateway.get_current_user_from_jwt(token)

    def test_should_raise_if_github_id_missing_in_jwt(self):
        user_repo = FakeUserRepository()
        gateway = FakeAuthenticationGateway(user_repo)
        token = "token_missing_github_id"
        gateway._last_payload = {"user_id": "user-123"}
        with pytest.raises(ValueError):
            gateway.get_current_user_from_jwt(token)

    def test_should_raise_if_user_not_found(self):
        user_repo = FakeUserRepository()
        gateway = FakeAuthenticationGateway(user_repo)
        user = User(user_id=UserId("user-123"), name="fakeuser", github_id=1)
        token = gateway.create_jwt(user)
        with pytest.raises(ValueError):
            gateway.get_current_user_from_jwt(token)

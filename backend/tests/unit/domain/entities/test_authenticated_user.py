# TDD-first: Tests for AuthenticatedUser entity (Clean Architecture, DDD)
import pytest

from sightcall_transcript_to_tutorial.domain.entities.authenticated_user import AuthenticatedUser


class TestAuthenticatedUser:
    def test_instantiation_with_valid_data(self):
        user = AuthenticatedUser(github_id=12345, username="octocat", email="octocat@github.com")
        assert user.github_id == 12345
        assert user.username == "octocat"
        assert user.email == "octocat@github.com"

    def test_missing_github_id_raises(self):
        with pytest.raises(ValueError):
            AuthenticatedUser(github_id=None, username="octocat", email="octocat@github.com")

    def test_invalid_email_raises(self):
        with pytest.raises(ValueError):
            AuthenticatedUser(github_id=12345, username="octocat", email="not-an-email")

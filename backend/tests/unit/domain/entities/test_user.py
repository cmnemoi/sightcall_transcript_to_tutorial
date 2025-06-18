import pytest

from sightcall_transcript_to_tutorial.domain.entities import User
from sightcall_transcript_to_tutorial.domain.value_objects import UserId


class TestUser:
    def test_should_create_user_with_valid_id_and_name(self):
        user = User(UserId("user-1"), name="Alice")
        assert user.user_id == UserId("user-1")
        assert user.name == "Alice"

    def test_should_be_equal_if_same_id_and_name(self):
        assert User(UserId("u1"), name="A") == User(UserId("u1"), name="A")
        assert User(UserId("u1"), name="A") != User(UserId("u2"), name="A")

    def test_should_raise_if_name_empty(self):
        with pytest.raises(ValueError):
            User(UserId("u1"), name="")

import pytest

from sightcall_transcript_to_tutorial.domain.value_objects import UserId


class TestUserId:
    def test_valid_user_id(self):
        uid = UserId("user-123")
        assert uid.value == "user-123"

    def test_equality(self):
        assert UserId("user-1") == UserId("user-1")
        assert UserId("user-1") != UserId("user-2")

    def test_invalid_user_id(self):
        with pytest.raises(ValueError):
            UserId("")

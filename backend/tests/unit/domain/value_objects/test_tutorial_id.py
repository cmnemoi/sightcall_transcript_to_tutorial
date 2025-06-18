import pytest

from sightcall_transcript_to_tutorial.domain.value_objects import TutorialId


class TestTutorialId:
    def test_valid_tutorial_id(self):
        tid = TutorialId("tutorial-xyz")
        assert tid.value == "tutorial-xyz"

    def test_equality(self):
        assert TutorialId("tut1") == TutorialId("tut1")
        assert TutorialId("tut1") != TutorialId("tut2")

    def test_invalid_tutorial_id(self):
        with pytest.raises(ValueError):
            TutorialId("")

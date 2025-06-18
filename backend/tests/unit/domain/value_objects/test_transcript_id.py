import pytest

from sightcall_transcript_to_tutorial.domain.value_objects import TranscriptId


class TestTranscriptId:
    def test_valid_transcript_id(self):
        tid = TranscriptId("transcript-abc")
        assert tid.value == "transcript-abc"

    def test_equality(self):
        assert TranscriptId("t1") == TranscriptId("t1")
        assert TranscriptId("t1") != TranscriptId("t2")

    def test_invalid_transcript_id(self):
        with pytest.raises(ValueError):
            TranscriptId("")

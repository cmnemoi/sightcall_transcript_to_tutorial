import pytest

from sightcall_transcript_to_tutorial.domain.entities import Transcript
from sightcall_transcript_to_tutorial.domain.exceptions.tutorial_generation_error import InvalidTranscriptError
from sightcall_transcript_to_tutorial.domain.value_objects import TranscriptId
from sightcall_transcript_to_tutorial.domain.value_objects.transcript_content import TranscriptContent


class TestTranscript:
    def test_should_create_transcript_with_valid_id_and_content(self):
        valid_content = '{"timestamp": "2025-02-26T20:36:06Z", "duration_in_ticks": 12345, "phrases": [{"offset_milliseconds": 0, "duration_in_ticks": 1.0, "display": "Hello", "speaker": 1, "locale": "en-US", "confidence": 0.9}]}'
        tc = TranscriptContent(valid_content)
        transcript = Transcript(TranscriptId("t1"), content=tc)
        assert transcript.transcript_id == TranscriptId("t1")
        assert transcript.content == tc

    def test_should_be_equal_if_same_id_and_content(self):
        valid_content = '{"timestamp": "2025-02-26T20:36:06Z", "duration_in_ticks": 12345, "phrases": [{"offset_milliseconds": 0, "duration_in_ticks": 1.0, "display": "Hello", "speaker": 1, "locale": "en-US", "confidence": 0.9}]}'
        tc = TranscriptContent(valid_content)
        assert Transcript(TranscriptId("t1"), content=tc) == Transcript(TranscriptId("t1"), content=tc)
        other_content = '{"timestamp": "2025-02-26T20:36:06Z", "duration_in_ticks": 12345, "phrases": [{"offset_milliseconds": 0, "duration_in_ticks": 1.0, "display": "Bye", "speaker": 2, "locale": "en-US", "confidence": 0.8}]}'
        tc2 = TranscriptContent(other_content)
        assert Transcript(TranscriptId("t1"), content=tc) != Transcript(TranscriptId("t2"), content=tc2)

    def test_should_raise_if_content_empty(self):
        with pytest.raises(InvalidTranscriptError):
            TranscriptContent("")

    def test_should_create_transcript_with_valid_json_content(self):
        valid_content = '{"timestamp": "2025-02-26T20:36:06Z", "duration_in_ticks": 12345, "phrases": [{"offset_milliseconds": 0, "duration_in_ticks": 1.0, "display": "Hello", "speaker": 1, "locale": "en-US", "confidence": 0.9}]}'
        tc = TranscriptContent(valid_content)
        transcript = Transcript(TranscriptId("t2"), content=tc)
        assert transcript.content == tc

    def test_should_raise_if_missing_required_fields(self):
        # Missing 'timestamp' field
        invalid_content = '{"duration_in_ticks": 12345, "phrases": [{"offset_milliseconds": 0, "duration_in_ticks": 1.0, "display": "Hello", "speaker": 1, "locale": "en-US", "confidence": 0.9}]}'
        with pytest.raises(InvalidTranscriptError):
            TranscriptContent(invalid_content)

    def test_should_raise_if_invalid_json(self):
        invalid_json = '{speaker: "Alice", text: "Hello"}'  # Not valid JSON
        with pytest.raises(InvalidTranscriptError):
            TranscriptContent(invalid_json)

    def test_should_raise_if_content_too_large(self):
        oversized_content = (
            '{"timestamp": "2025-02-26T20:36:06Z", "duration_in_ticks": 12345, "phrases": [{"offset_milliseconds": 0, "duration_in_ticks": 1.0, "display": "'
            + ("A" * 1_000_000)
            + '", "speaker": 1, "locale": "en-US", "confidence": 0.9}]}'
        )
        with pytest.raises(InvalidTranscriptError):
            TranscriptContent(oversized_content)

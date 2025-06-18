import pytest

from sightcall_transcript_to_tutorial.domain.exceptions.tutorial_generation_error import InvalidTranscriptError
from sightcall_transcript_to_tutorial.domain.value_objects.transcript_content import TranscriptContent


class TestTranscriptContent:
    def test_should_create_with_valid_transcript_json(self):
        valid_content = '{"timestamp": "2025-02-26T20:36:06Z", "duration_in_ticks": 12345, "phrases": [{"offset_milliseconds": 0, "duration_in_ticks": 1.0, "display": "Hello", "speaker": 1, "locale": "en-US", "confidence": 0.9}]}'
        tc = TranscriptContent(valid_content)
        assert tc.timestamp == "2025-02-26T20:36:06Z"
        assert tc.duration_in_ticks == 12345
        assert isinstance(tc.phrases, list)
        assert tc.phrases[0]["display"] == "Hello"

    def test_should_raise_if_missing_required_fields(self):
        # Missing 'timestamp'
        invalid_content = '{"duration_in_ticks": 12345, "phrases": [{"offset_milliseconds": 0, "duration_in_ticks": 1.0, "display": "Hello", "speaker": 1, "locale": "en-US", "confidence": 0.9}]}'
        with pytest.raises(InvalidTranscriptError):
            TranscriptContent(invalid_content)

    def test_should_raise_if_invalid_json(self):
        invalid_json = '{timestamp: "2025-02-26T20:36:06Z", duration_in_ticks: 12345}'
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

    def test_should_be_equal_if_same_content(self):
        content = '{"timestamp": "2025-02-26T20:36:06Z", "duration_in_ticks": 12345, "phrases": [{"offset_milliseconds": 0, "duration_in_ticks": 1.0, "display": "Hello", "speaker": 1, "locale": "en-US", "confidence": 0.9}]}'
        assert TranscriptContent(content) == TranscriptContent(content)

    def test_should_be_immutable(self):
        content = '{"timestamp": "2025-02-26T20:36:06Z", "duration_in_ticks": 12345, "phrases": [{"offset_milliseconds": 0, "duration_in_ticks": 1.0, "display": "Hello", "speaker": 1, "locale": "en-US", "confidence": 0.9}]}'
        tc = TranscriptContent(content)
        with pytest.raises(AttributeError):
            tc.timestamp = "2026-01-01T00:00:00Z"

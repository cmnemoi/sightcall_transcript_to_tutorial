import json
from dataclasses import dataclass, field
from typing import Any

from sightcall_transcript_to_tutorial.domain.exceptions.tutorial_generation_error import InvalidTranscriptError

MAX_TRANSCRIPT_SIZE_BYTES = 100 * 1024  # 100KB


@dataclass(frozen=True, eq=True)
class TranscriptContent:
    """
    Value object representing the validated content of a transcript upload.
    Encapsulates parsing, validation, and access to transcript metadata and phrases.
    """

    _raw_content: str = field(repr=False)
    _data: dict = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        object.__setattr__(self, "_data", self._parse_and_validate(self._raw_content))

    @staticmethod
    def _parse_and_validate(raw_content: str) -> dict:
        TranscriptContent._validate_not_empty(raw_content)
        TranscriptContent._validate_size_limit(raw_content)
        data = TranscriptContent._parse_json(raw_content)
        TranscriptContent._validate_schema(data)
        return data

    @staticmethod
    def _validate_not_empty(content: str) -> None:
        if not TranscriptContent._is_non_empty_str(content):
            raise InvalidTranscriptError("Transcript content must be a non-empty string.")

    @staticmethod
    def _validate_size_limit(content: str) -> None:
        if len(content.encode("utf-8")) > MAX_TRANSCRIPT_SIZE_BYTES:
            raise InvalidTranscriptError(
                f"Transcript content exceeds maximum allowed size ({MAX_TRANSCRIPT_SIZE_BYTES} bytes)."
            )

    @staticmethod
    def _parse_json(content: str) -> dict:
        try:
            data = json.loads(content)
        except Exception:
            raise InvalidTranscriptError("Transcript content must be valid JSON.")
        if not isinstance(data, dict):
            raise InvalidTranscriptError("Transcript JSON must be a JSON object at the top level.")
        return data

    @staticmethod
    def _validate_schema(data: dict) -> None:
        required_fields = ["timestamp", "duration_in_ticks", "phrases"]
        for data_field in required_fields:
            if data_field not in data:
                raise InvalidTranscriptError(f"Missing required field: '{data_field}'.")
        if not TranscriptContent._is_non_empty_str(data["timestamp"]):
            raise InvalidTranscriptError("'timestamp' must be a non-empty string.")
        if not TranscriptContent._is_number(data["duration_in_ticks"]):
            raise InvalidTranscriptError("'duration_in_ticks' must be a number.")
        if not TranscriptContent._is_non_empty_list(data["phrases"]):
            raise InvalidTranscriptError("'phrases' must be a non-empty list.")
        for idx, phrase in enumerate(data["phrases"]):
            TranscriptContent._validate_phrase(phrase, idx)

    @staticmethod
    def _validate_phrase(phrase: Any, idx: int) -> None:
        if not isinstance(phrase, dict):
            raise InvalidTranscriptError(f"Each phrase must be a JSON object (error at index {idx}).")
        required_phrase_fields: list[tuple[str, type | tuple[type, ...]]] = [
            ("offset_milliseconds", int),
            ("duration_in_ticks", (int, float)),
            ("display", str),
            ("speaker", int),
            ("locale", str),
            ("confidence", float),
        ]
        for phrase_field, expected_type in required_phrase_fields:
            if phrase_field not in phrase:
                raise InvalidTranscriptError(f"Phrase at index {idx} missing required field: '{phrase_field}'.")
            if not isinstance(phrase[phrase_field], expected_type):
                type_name = TranscriptContent._type_name(expected_type)
                raise InvalidTranscriptError(
                    f"Phrase field '{phrase_field}' at index {idx} has wrong type (expected {type_name})."
                )

    @staticmethod
    def _type_name(expected_type: type | tuple[type, ...]) -> str:
        if isinstance(expected_type, tuple):
            return ", ".join(t.__name__ for t in expected_type if isinstance(t, type))
        if isinstance(expected_type, type):
            return expected_type.__name__
        return str(expected_type)

    @property
    def timestamp(self) -> str:
        """Return the transcript's timestamp as a string."""
        return self._data["timestamp"]

    @property
    def duration_in_ticks(self) -> int:
        """Return the transcript's duration in ticks as an integer or float."""
        return self._data["duration_in_ticks"]

    @property
    def phrases(self) -> list:
        """Return the list of phrase dictionaries in the transcript."""
        return self._data["phrases"]

    def __str__(self) -> str:
        """Return the original raw JSON string for storage or serialization."""
        return self._raw_content

    @staticmethod
    def _is_number(value: Any) -> bool:
        return isinstance(value, (int, float))

    @staticmethod
    def _is_non_empty_str(value: Any) -> bool:
        return isinstance(value, str) and bool(value.strip())

    @staticmethod
    def _is_non_empty_list(value: Any) -> bool:
        return isinstance(value, list) and len(value) > 0

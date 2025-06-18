import pytest

from sightcall_transcript_to_tutorial.domain.entities import Transcript
from sightcall_transcript_to_tutorial.domain.value_objects import TranscriptId
from sightcall_transcript_to_tutorial.domain.value_objects.transcript_content import TranscriptContent
from sightcall_transcript_to_tutorial.infrastructure.for_production.repositories.sqlalchemy_transcript_repository import (
    SQLAlchemyTranscriptRepository,
)


@pytest.mark.integration
def test_sqlalchemy_transcript_repository(pg_session):
    repo = SQLAlchemyTranscriptRepository(pg_session)
    valid_content = '{"timestamp": "2025-02-26T20:36:06Z", "duration_in_ticks": 12345, "phrases": [{"offset_milliseconds": 0, "duration_in_ticks": 1.0, "display": "Hello", "speaker": 1, "locale": "en-US", "confidence": 0.9}]}'
    transcript = Transcript(TranscriptId("t1"), content=TranscriptContent(valid_content))
    repo.save(transcript)
    fetched = repo.find_by_id(TranscriptId("t1"))
    assert fetched == transcript
    repo.delete(TranscriptId("t1"))
    assert repo.find_by_id(TranscriptId("t1")) is None

from sightcall_transcript_to_tutorial.domain.entities import Transcript
from sightcall_transcript_to_tutorial.domain.value_objects import TranscriptId
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_transcript_repository import (
    FakeTranscriptRepository,
)


class TestFakeTranscriptRepository:
    def test_save_and_find_by_id(self):
        repo = FakeTranscriptRepository()
        transcript = Transcript(TranscriptId("t1"), content="Hello")
        repo.save(transcript)
        assert repo.find_by_id(TranscriptId("t1")) == transcript

    def test_find_by_id_not_found(self):
        repo = FakeTranscriptRepository()
        assert repo.find_by_id(TranscriptId("missing")) is None

    def test_delete(self):
        repo = FakeTranscriptRepository()
        transcript = Transcript(TranscriptId("t1"), content="Hello")
        repo.save(transcript)
        repo.delete(TranscriptId("t1"))
        assert repo.find_by_id(TranscriptId("t1")) is None

    def test_delete_nonexistent(self):
        repo = FakeTranscriptRepository()
        repo.delete(TranscriptId("doesnotexist"))

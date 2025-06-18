from sightcall_transcript_to_tutorial.domain.entities import Transcript
from sightcall_transcript_to_tutorial.domain.repositories import TranscriptRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects import TranscriptId


class FakeTranscriptRepository(TranscriptRepositoryInterface):
    """
    In-memory fake repository for Transcript entities.
    Stores TranscriptContent as value object, keyed by transcript_id.value.
    """

    def __init__(self):
        self._transcripts: dict[str, Transcript] = {}

    def find_by_id(self, transcript_id: TranscriptId) -> Transcript | None:
        return self._transcripts.get(transcript_id.value)

    def save(self, transcript: Transcript) -> None:
        self._transcripts[transcript.transcript_id.value] = transcript

    def delete(self, transcript_id: TranscriptId) -> None:
        self._transcripts.pop(transcript_id.value, None)

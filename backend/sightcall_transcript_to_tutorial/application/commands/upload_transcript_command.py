from sightcall_transcript_to_tutorial.domain.entities.transcript import Transcript
from sightcall_transcript_to_tutorial.domain.entities.user import User
from sightcall_transcript_to_tutorial.domain.repositories.transcript_repository_interface import (
    TranscriptRepositoryInterface,
)
from sightcall_transcript_to_tutorial.domain.value_objects.transcript_content import TranscriptContent
from sightcall_transcript_to_tutorial.domain.value_objects.transcript_id import TranscriptId


class UploadTranscriptCommand:
    def __init__(self, user: User, content: TranscriptContent):
        self.user = user
        self.content = content


class UploadTranscriptCommandHandler:
    def __init__(self, transcript_repository: TranscriptRepositoryInterface):
        self._repo = transcript_repository

    def handle(self, command: UploadTranscriptCommand) -> TranscriptId:
        transcript = Transcript(TranscriptId.generate(), command.content)
        self._repo.save(transcript)
        return transcript.transcript_id

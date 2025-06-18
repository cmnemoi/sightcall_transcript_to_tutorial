import pytest

from sightcall_transcript_to_tutorial.application.commands.upload_transcript_command import (
    UploadTranscriptCommand,
    UploadTranscriptCommandHandler,
)
from sightcall_transcript_to_tutorial.domain.entities.user import User
from sightcall_transcript_to_tutorial.domain.exceptions.tutorial_generation_error import InvalidTranscriptError
from sightcall_transcript_to_tutorial.domain.value_objects.transcript_content import TranscriptContent
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_transcript_repository import (
    FakeTranscriptRepository,
)


class TestUploadTranscriptCommandHandler:
    def given_valid_transcript_content(self):
        return TranscriptContent(
            '{"timestamp": "2025-02-26T20:36:06Z", "duration_in_ticks": 12345, "phrases": [{"offset_milliseconds": 0, "duration_in_ticks": 1.0, "display": "Hello", "speaker": 1, "locale": "en-US", "confidence": 0.9}]}'
        )

    def given_user(self):
        return User(user_id=UserId("u1"), name="alice")

    def test_should_upload_transcript_successfully(self):
        # Given
        repo = FakeTranscriptRepository()
        handler = UploadTranscriptCommandHandler(repo)
        user = self.given_user()
        content = self.given_valid_transcript_content()
        command = UploadTranscriptCommand(user=user, content=content)
        # When
        transcript_id = handler.handle(command)
        # Then
        stored = repo.find_by_id(transcript_id)
        assert stored is not None
        assert stored.content == content
        assert stored.transcript_id == transcript_id

    def test_should_raise_if_invalid_transcript_content(self):
        repo = FakeTranscriptRepository()
        UploadTranscriptCommandHandler(repo)
        user = self.given_user()
        with pytest.raises(InvalidTranscriptError):
            # Invalid content (empty string)
            UploadTranscriptCommand(user=user, content=TranscriptContent(""))

    def test_should_propagate_repository_error(self):
        class FailingRepo(FakeTranscriptRepository):
            def save(self, transcript):
                raise RuntimeError("DB error")

        repo = FailingRepo()
        handler = UploadTranscriptCommandHandler(repo)
        user = self.given_user()
        content = self.given_valid_transcript_content()
        command = UploadTranscriptCommand(user=user, content=content)
        with pytest.raises(RuntimeError):
            handler.handle(command)

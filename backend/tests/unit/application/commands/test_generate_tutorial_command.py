import pytest

from sightcall_transcript_to_tutorial.application.commands.generate_tutorial_command import (
    GenerateTutorialCommand,
    GenerateTutorialCommandHandler,
)
from sightcall_transcript_to_tutorial.domain.entities.transcript import Transcript
from sightcall_transcript_to_tutorial.domain.entities.tutorial import Tutorial
from sightcall_transcript_to_tutorial.domain.exceptions.tutorial_generation_error import TutorialGenerationError
from sightcall_transcript_to_tutorial.domain.value_objects.transcript_id import TranscriptId
from sightcall_transcript_to_tutorial.domain.value_objects.tutorial_id import TutorialId
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_transcript_repository import (
    FakeTranscriptRepository,
)
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_tutorial_repository import (
    FakeTutorialRepository,
)


class _FakeTutorialGeneratorGateway:
    def __init__(self, should_fail: bool = False):
        self._should_fail = should_fail
        self.called_with = None
        self.called_with_user_id = None

    def generate_tutorial(self, transcript: Transcript, user_id: UserId) -> Tutorial:
        self.called_with = transcript
        self.called_with_user_id = user_id
        if self._should_fail:
            raise TutorialGenerationError("AI error")
        return Tutorial(
            tutorial_id=TutorialId("tut1"),
            title="Generated Tutorial",
            content="AI generated content",
            user_id=user_id,
        )


class TestGenerateTutorialCommandHandler:
    def test_should_generate_tutorial_with_correct_user_id(self):
        # Given
        user_id = UserId("user-123")
        transcript = self._given_transcript()
        transcript_repo = self._given_transcript_repository_with_transcript(transcript)
        tutorial_generator_gateway = self._given_tutorial_generator_gateway()
        tutorial_repo = self._given_tutorial_repository()
        handler = self._given_handler(transcript_repo, tutorial_generator_gateway, tutorial_repo)
        command = GenerateTutorialCommand(transcript_id="tr1", user_id=user_id)

        # When
        tutorial = self._when_handle_command(handler, command)

        # Then
        self._then_tutorial_should_be_generated_with_user_id(tutorial, user_id)
        self._then_gateway_should_be_called_with_user_id(tutorial_generator_gateway, user_id)

    def test_should_generate_tutorial_successfully(self):
        # Given
        user_id = UserId("user-123")
        transcript = self._given_transcript()
        transcript_repo = self._given_transcript_repository_with_transcript(transcript)
        tutorial_generator_gateway = self._given_tutorial_generator_gateway()
        tutorial_repo = self._given_tutorial_repository()
        handler = self._given_handler(transcript_repo, tutorial_generator_gateway, tutorial_repo)
        command = GenerateTutorialCommand(transcript_id="tr1", user_id=user_id)

        # When
        tutorial = self._when_handle_command(handler, command)

        # Then
        self._then_tutorial_should_be_generated(tutorial, "Generated Tutorial", "AI generated content")
        self._then_gateway_should_be_called_with_transcript(tutorial_generator_gateway, transcript)

    def test_should_raise_error_when_gateway_fails(self):
        # Given
        user_id = UserId("user-123")
        transcript = self._given_transcript()
        transcript_repo = self._given_transcript_repository_with_transcript(transcript)
        tutorial_generator_gateway = self._given_failing_tutorial_generator_gateway()
        tutorial_repo = self._given_tutorial_repository()
        handler = self._given_handler(transcript_repo, tutorial_generator_gateway, tutorial_repo)
        command = GenerateTutorialCommand(transcript_id="tr1", user_id=user_id)

        # When & Then
        with pytest.raises(TutorialGenerationError):
            self._when_handle_command(handler, command)

    def test_should_persist_generated_tutorial_in_repository(self):
        # Given
        user_id = UserId("user-123")
        transcript = self._given_transcript()
        transcript_repo = self._given_transcript_repository_with_transcript(transcript)
        tutorial_generator_gateway = self._given_tutorial_generator_gateway()
        tutorial_repo = self._given_tutorial_repository()
        handler = self._given_handler(transcript_repo, tutorial_generator_gateway, tutorial_repo)
        command = GenerateTutorialCommand(transcript_id="tr1", user_id=user_id)

        # When
        tutorial = self._when_handle_command(handler, command)

        # Then
        self._then_tutorial_should_be_persisted(tutorial_repo, tutorial)

    def _given_transcript(self) -> Transcript:
        return Transcript(TranscriptId("tr1"), "Sample transcript")

    def _given_transcript_repository_with_transcript(self, transcript: Transcript) -> FakeTranscriptRepository:
        repo = FakeTranscriptRepository()
        repo.save(transcript)
        return repo

    def _given_tutorial_generator_gateway(self) -> _FakeTutorialGeneratorGateway:
        return _FakeTutorialGeneratorGateway()

    def _given_failing_tutorial_generator_gateway(self) -> _FakeTutorialGeneratorGateway:
        return _FakeTutorialGeneratorGateway(should_fail=True)

    def _given_tutorial_repository(self) -> FakeTutorialRepository:
        return FakeTutorialRepository()

    def _given_handler(
        self,
        transcript_repo: FakeTranscriptRepository,
        gateway: _FakeTutorialGeneratorGateway,
        tutorial_repo: FakeTutorialRepository,
    ) -> GenerateTutorialCommandHandler:
        return GenerateTutorialCommandHandler(transcript_repo, gateway, tutorial_repo)

    def _when_handle_command(
        self, handler: GenerateTutorialCommandHandler, command: GenerateTutorialCommand
    ) -> Tutorial:
        return handler.handle(command)

    def _then_tutorial_should_be_generated(
        self, tutorial: Tutorial, expected_title: str, expected_content: str
    ) -> None:
        assert tutorial.title == expected_title
        assert tutorial.content == expected_content

    def _then_tutorial_should_be_generated_with_user_id(self, tutorial: Tutorial, expected_user_id: UserId) -> None:
        assert tutorial.user_id == expected_user_id

    def _then_gateway_should_be_called_with_transcript(
        self, gateway: _FakeTutorialGeneratorGateway, expected_transcript: Transcript
    ) -> None:
        assert gateway.called_with == expected_transcript

    def _then_gateway_should_be_called_with_user_id(
        self, gateway: _FakeTutorialGeneratorGateway, expected_user_id: UserId
    ) -> None:
        assert gateway.called_with_user_id == expected_user_id

    def _then_tutorial_should_be_persisted(self, tutorial_repo: FakeTutorialRepository, tutorial: Tutorial) -> None:
        persisted_tutorial = tutorial_repo.find_by_id(tutorial.tutorial_id)
        assert persisted_tutorial == tutorial

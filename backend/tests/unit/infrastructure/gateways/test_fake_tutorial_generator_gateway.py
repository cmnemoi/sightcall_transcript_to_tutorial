import pytest

from sightcall_transcript_to_tutorial.domain.entities.transcript import Transcript
from sightcall_transcript_to_tutorial.domain.entities.tutorial import Tutorial
from sightcall_transcript_to_tutorial.domain.exceptions.tutorial_generation_error import TutorialGenerationError
from sightcall_transcript_to_tutorial.domain.value_objects.transcript_id import TranscriptId
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId
from sightcall_transcript_to_tutorial.infrastructure.for_tests.gateways.fake_tutorial_generator_gateway import (
    FakeTutorialGeneratorGateway,
)


class TestFakeTutorialGeneratorGateway:
    def test_should_generate_fake_tutorial_successfully(self):
        # Given
        gateway = self._given_gateway()
        transcript = self._given_transcript()
        user_id = self._given_user_id()

        # When
        tutorial = self._when_generate_tutorial(gateway, transcript, user_id)

        # Then
        self._then_tutorial_should_be_valid(tutorial)
        self._then_tutorial_should_have_expected_properties(
            tutorial, "Fake Tutorial", "This is a fake tutorial for testing.", user_id
        )

    def test_should_raise_error_when_simulated_failure_enabled(self):
        # Given
        gateway = self._given_failing_gateway()
        transcript = self._given_transcript()
        user_id = self._given_user_id()

        # When & Then
        with pytest.raises(TutorialGenerationError):
            self._when_generate_tutorial(gateway, transcript, user_id)

    def _given_gateway(self) -> FakeTutorialGeneratorGateway:
        return FakeTutorialGeneratorGateway()

    def _given_failing_gateway(self) -> FakeTutorialGeneratorGateway:
        return FakeTutorialGeneratorGateway(should_fail=True)

    def _given_transcript(self) -> Transcript:
        return Transcript(TranscriptId("tr1"), "Sample transcript")

    def _given_user_id(self) -> UserId:
        return UserId("user-123")

    def _when_generate_tutorial(
        self, gateway: FakeTutorialGeneratorGateway, transcript: Transcript, user_id: UserId
    ) -> Tutorial:
        return gateway.generate_tutorial(transcript, user_id)

    def _then_tutorial_should_be_valid(self, tutorial: Tutorial) -> None:
        assert isinstance(tutorial, Tutorial)

    def _then_tutorial_should_have_expected_properties(
        self, tutorial: Tutorial, expected_title: str, expected_content: str, expected_user_id: UserId
    ) -> None:
        assert tutorial.title == expected_title
        assert tutorial.content == expected_content
        assert tutorial.user_id == expected_user_id

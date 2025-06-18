from sightcall_transcript_to_tutorial.domain.entities.transcript import Transcript
from sightcall_transcript_to_tutorial.domain.entities.tutorial import Tutorial
from sightcall_transcript_to_tutorial.domain.exceptions.tutorial_generation_error import TutorialGenerationError
from sightcall_transcript_to_tutorial.domain.gateways.tutorial_generator_gateway_interface import (
    TutorialGeneratorGatewayInterface,
)
from sightcall_transcript_to_tutorial.domain.value_objects.tutorial_id import TutorialId
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId


class FakeTutorialGeneratorGateway(TutorialGeneratorGatewayInterface):
    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail

    def generate_tutorial(self, transcript: Transcript, user_id: UserId) -> Tutorial:
        if self.should_fail:
            raise TutorialGenerationError("Simulated failure in fake gateway.")
        return Tutorial(
            tutorial_id=TutorialId("fake-tut-1"),
            title="Fake Tutorial",
            content="This is a fake tutorial for testing.",
            user_id=user_id,
        )

from sightcall_transcript_to_tutorial.domain.entities.tutorial import Tutorial
from sightcall_transcript_to_tutorial.domain.gateways.tutorial_generator_gateway_interface import (
    TutorialGeneratorGatewayInterface,
)
from sightcall_transcript_to_tutorial.domain.repositories.transcript_repository_interface import (
    TranscriptRepositoryInterface,
)
from sightcall_transcript_to_tutorial.domain.repositories.tutorial_repository_interface import (
    TutorialRepositoryInterface,
)
from sightcall_transcript_to_tutorial.domain.value_objects.transcript_id import TranscriptId
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId


class GenerateTutorialCommand:
    def __init__(self, transcript_id: str, user_id: UserId):
        self.transcript_id = transcript_id
        self.user_id = user_id


class GenerateTutorialCommandHandler:
    def __init__(
        self,
        transcript_repository: TranscriptRepositoryInterface,
        generate_tutorial_gateway: TutorialGeneratorGatewayInterface,
        tutorial_repository: TutorialRepositoryInterface,
    ):
        self.transcript_repository = transcript_repository
        self.generate_tutorial_gateway = generate_tutorial_gateway
        self.tutorial_repository = tutorial_repository

    def handle(self, command: GenerateTutorialCommand) -> Tutorial:
        transcript = self.transcript_repository.find_by_id(TranscriptId(command.transcript_id))
        if not transcript:
            raise ValueError(f"Transcript with id {command.transcript_id} not found")
        tutorial = self.generate_tutorial_gateway.generate_tutorial(transcript, command.user_id)
        self.tutorial_repository.save(tutorial)
        return tutorial

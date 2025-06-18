from abc import ABC, abstractmethod

from sightcall_transcript_to_tutorial.domain.entities.transcript import Transcript
from sightcall_transcript_to_tutorial.domain.entities.tutorial import Tutorial
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId


class TutorialGeneratorGatewayInterface(ABC):
    @abstractmethod
    def generate_tutorial(self, transcript: Transcript, user_id: UserId) -> Tutorial:
        """Generate a tutorial from a transcript using an AI service."""
        pass

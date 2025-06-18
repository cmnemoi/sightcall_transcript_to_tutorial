from abc import ABC, abstractmethod

from sightcall_transcript_to_tutorial.domain.entities import Transcript
from sightcall_transcript_to_tutorial.domain.value_objects import TranscriptId


class TranscriptRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, transcript_id: TranscriptId) -> Transcript | None:
        pass

    @abstractmethod
    def save(self, transcript: Transcript) -> None:
        pass

    @abstractmethod
    def delete(self, transcript_id: TranscriptId) -> None:
        pass

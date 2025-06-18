from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from sightcall_transcript_to_tutorial.domain.entities import Transcript
from sightcall_transcript_to_tutorial.domain.value_objects import TranscriptId
from sightcall_transcript_to_tutorial.domain.value_objects.transcript_content import TranscriptContent
from sightcall_transcript_to_tutorial.infrastructure.for_production.models.base import Base


class SQLAlchemyTranscript(Base):
    __tablename__ = "transcripts"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    content: Mapped[str] = mapped_column(String, nullable=False)

    @staticmethod
    def from_domain(transcript: Transcript) -> "SQLAlchemyTranscript":
        return SQLAlchemyTranscript(id=transcript.transcript_id.value, content=str(transcript.content))

    def to_domain(self) -> Transcript:
        return Transcript(TranscriptId(self.id), content=TranscriptContent(self.content))

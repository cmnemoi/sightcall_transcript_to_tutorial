from sqlalchemy.orm import Session

from sightcall_transcript_to_tutorial.domain.entities import Transcript
from sightcall_transcript_to_tutorial.domain.repositories import TranscriptRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects import TranscriptId
from sightcall_transcript_to_tutorial.infrastructure.for_production.models.sqlalchemy_transcript import (
    SQLAlchemyTranscript,
)


class SQLAlchemyTranscriptRepository(TranscriptRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def find_by_id(self, transcript_id: TranscriptId) -> Transcript | None:
        row = self._session.query(SQLAlchemyTranscript).filter_by(id=transcript_id.value).first()
        return row.to_domain() if row else None

    def save(self, transcript: Transcript) -> None:
        obj = self._session.query(SQLAlchemyTranscript).filter_by(id=transcript.transcript_id.value).first()
        if obj:
            obj.content = str(transcript.content)
        else:
            obj = SQLAlchemyTranscript.from_domain(transcript)
            self._session.add(obj)
        self._session.commit()

    def delete(self, transcript_id: TranscriptId) -> None:
        obj = self._session.query(SQLAlchemyTranscript).filter_by(id=transcript_id.value).first()
        if obj:
            self._session.delete(obj)
            self._session.commit()

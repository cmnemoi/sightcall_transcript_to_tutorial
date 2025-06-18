import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from sightcall_transcript_to_tutorial.domain.entities import Tutorial
from sightcall_transcript_to_tutorial.domain.value_objects import TutorialId, UserId
from sightcall_transcript_to_tutorial.infrastructure.for_production.models.base import Base


class SQLAlchemyTutorial(Base):
    __tablename__ = "tutorials"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False, default="")
    user_id: Mapped[str] = mapped_column(String, nullable=False, default="user-1")
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.timezone.utc)
    )

    @staticmethod
    def from_domain(tutorial: Tutorial) -> "SQLAlchemyTutorial":
        return SQLAlchemyTutorial(
            id=tutorial.tutorial_id.value,
            title=tutorial.title,
            content=tutorial.content,
            user_id=tutorial.user_id.value,
            created_at=tutorial.created_at,
            updated_at=tutorial.updated_at,
        )

    def to_domain(self) -> Tutorial:
        return Tutorial(
            TutorialId(self.id),
            title=self.title,
            content=self.content,
            user_id=UserId(self.user_id),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

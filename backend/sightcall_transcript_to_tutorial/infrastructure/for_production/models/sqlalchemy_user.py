from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from sightcall_transcript_to_tutorial.domain.entities import User
from sightcall_transcript_to_tutorial.domain.value_objects import UserId
from sightcall_transcript_to_tutorial.infrastructure.for_production.models.base import Base


class SQLAlchemyUser(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    github_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    @classmethod
    def from_domain(cls, user: User) -> "SQLAlchemyUser":
        return cls(
            id=user.user_id.value,
            name=user.name,
            github_id=user.github_id,
        )

    def to_domain(self) -> User:
        return User(
            user_id=UserId(self.id),
            name=self.name,
            github_id=self.github_id,
        )

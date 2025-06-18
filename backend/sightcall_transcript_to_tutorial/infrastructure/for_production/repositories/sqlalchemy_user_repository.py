from sqlalchemy.orm import Session

from sightcall_transcript_to_tutorial.domain.entities import User
from sightcall_transcript_to_tutorial.domain.repositories import UserRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects import UserId
from sightcall_transcript_to_tutorial.infrastructure.for_production.models.sqlalchemy_user import SQLAlchemyUser


class SQLAlchemyUserRepository(UserRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def find_by_id(self, user_id: UserId) -> User | None:
        row = self._session.query(SQLAlchemyUser).filter_by(id=user_id.value).first()
        return row.to_domain() if row else None

    def save(self, user: User) -> None:
        obj = self._session.query(SQLAlchemyUser).filter_by(id=user.user_id.value).first()
        if obj:
            obj.name = user.name
            obj.github_id = user.github_id
        else:
            obj = SQLAlchemyUser.from_domain(user)
            self._session.add(obj)
        self._session.commit()

    def delete(self, user_id: UserId) -> None:
        obj = self._session.query(SQLAlchemyUser).filter_by(id=user_id.value).first()
        if obj:
            self._session.delete(obj)
            self._session.commit()

    def find_by_github_id(self, github_id: int) -> User | None:
        obj = self._session.query(SQLAlchemyUser).filter_by(github_id=github_id).first()
        return obj.to_domain() if obj else None

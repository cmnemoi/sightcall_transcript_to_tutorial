from typing import Any, Optional

from sqlalchemy.orm import Session

from sightcall_transcript_to_tutorial.domain.entities import Tutorial
from sightcall_transcript_to_tutorial.domain.repositories import TutorialRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects import TutorialId, UserId
from sightcall_transcript_to_tutorial.infrastructure.for_production.models.sqlalchemy_tutorial import (
    SQLAlchemyTutorial,
)


class SQLAlchemyTutorialRepository(TutorialRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def find_by_id(self, tutorial_id: TutorialId) -> Tutorial | None:
        row = self._session.query(SQLAlchemyTutorial).filter_by(id=tutorial_id.value).first()
        return row.to_domain() if row else None

    def save(self, tutorial: Tutorial) -> None:
        obj = self._session.query(SQLAlchemyTutorial).filter_by(id=tutorial.tutorial_id.value).first()
        if obj:
            obj.title = tutorial.title
            obj.content = tutorial.content
            obj.user_id = tutorial.user_id.value
            obj.updated_at = tutorial.updated_at
            obj.created_at = tutorial.created_at
        else:
            obj = SQLAlchemyTutorial.from_domain(tutorial)
            self._session.add(obj)
        self._session.commit()

    def delete(self, tutorial_id: TutorialId) -> None:
        obj = self._session.query(SQLAlchemyTutorial).filter_by(id=tutorial_id.value).first()
        if obj:
            self._session.delete(obj)
            self._session.commit()

    def list_tutorials(
        self,
        user_id: UserId,
        filters: Optional[dict[str, Any]] = None,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
    ) -> list[Tutorial]:
        query = self._session.query(SQLAlchemyTutorial).filter_by(user_id=user_id.value)
        if filters:
            if "created_at" in filters:
                query = query.filter(SQLAlchemyTutorial.created_at >= filters["created_at"])
            if "updated_at" in filters:
                query = query.filter(SQLAlchemyTutorial.updated_at >= filters["updated_at"])
        if search:
            query = query.filter(SQLAlchemyTutorial.title.ilike(f"%{search}%"))
        query = query.order_by(SQLAlchemyTutorial.created_at.desc())
        offset = (page - 1) * page_size
        rows = query.offset(offset).limit(page_size).all()
        return [row.to_domain() for row in rows]

    def update_tutorial(
        self,
        tutorial_id: TutorialId,
        user_id: UserId,
        title: Optional[str] = None,
        content: Optional[str] = None,
        updated_at: Any = None,
    ) -> Tutorial | None:
        obj = self._session.query(SQLAlchemyTutorial).filter_by(id=tutorial_id.value, user_id=user_id.value).first()
        if not obj:
            return None
        if title is not None:
            obj.title = title
        if content is not None:
            obj.content = content
        if updated_at is not None:
            obj.updated_at = updated_at
        self._session.commit()
        return obj.to_domain()

    def validate_ownership(self, tutorial_id: TutorialId, user_id: UserId) -> bool:
        obj = self._session.query(SQLAlchemyTutorial).filter_by(id=tutorial_id.value, user_id=user_id.value).first()
        return obj is not None

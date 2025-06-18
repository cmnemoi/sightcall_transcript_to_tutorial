import pytest

from sightcall_transcript_to_tutorial.domain.entities import User
from sightcall_transcript_to_tutorial.domain.value_objects import UserId
from sightcall_transcript_to_tutorial.infrastructure.for_production.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)


@pytest.mark.integration
def test_sqlalchemy_user_repository(pg_session):
    repo = SQLAlchemyUserRepository(pg_session)
    user = User(UserId("u1"), name="Alice")
    repo.save(user)
    fetched = repo.find_by_id(UserId("u1"))
    assert fetched == user
    repo.delete(UserId("u1"))
    assert repo.find_by_id(UserId("u1")) is None

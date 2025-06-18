from datetime import datetime, timezone

from sightcall_transcript_to_tutorial.application.queries.get_tutorial_by_id_query import (
    GetTutorialByIdQuery,
    GetTutorialByIdQueryHandler,
)
from sightcall_transcript_to_tutorial.domain.entities import Tutorial
from sightcall_transcript_to_tutorial.domain.repositories import TutorialRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects import TutorialId, UserId
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_tutorial_repository import (
    FakeTutorialRepository,
)


class TestGetTutorialByIdQueryHandler:
    def test_should_return_tutorial_when_user_is_owner(self):
        # Given
        repo = self._given_repository()
        user_id = UserId("user-1")
        tutorial = self._given_tutorial_in_repository(repo, "tut1", user_id)
        handler = self._given_handler(repo)
        query = self._given_query("tut1", user_id)

        # When
        result = self._when_handle_query(handler, query)

        # Then
        self._then_tutorial_should_equal(result, tutorial)

    def test_should_return_none_when_user_is_not_owner(self):
        # Given
        repo = self._given_repository()
        owner_user_id = UserId("user-1")
        non_owner_user_id = UserId("other-user")
        self._given_tutorial_in_repository(repo, "tut1", owner_user_id)
        handler = self._given_handler(repo)
        query = self._given_query("tut1", non_owner_user_id)

        # When
        result = self._when_handle_query(handler, query)

        # Then
        self._then_result_should_be_none(result)

    def test_should_return_none_when_tutorial_not_found(self):
        # Given
        repo = self._given_repository()
        handler = self._given_handler(repo)
        query = self._given_query("non-existent", UserId("user-1"))

        # When
        result = self._when_handle_query(handler, query)

        # Then
        self._then_result_should_be_none(result)

    def _given_repository(self) -> FakeTutorialRepository:
        return FakeTutorialRepository()

    def _given_tutorial_in_repository(
        self, repo: TutorialRepositoryInterface, tutorial_id: str, user_id: UserId
    ) -> Tutorial:
        now = datetime.now(timezone.utc)
        tutorial = Tutorial(
            tutorial_id=TutorialId(tutorial_id),
            title="Test Title",
            content="Test Content",
            user_id=user_id,
            created_at=now,
            updated_at=now,
        )
        repo.save(tutorial)
        return tutorial

    def _given_handler(self, repo: TutorialRepositoryInterface) -> GetTutorialByIdQueryHandler:
        return GetTutorialByIdQueryHandler(repo)

    def _given_query(self, tutorial_id: str, user_id: UserId) -> GetTutorialByIdQuery:
        return GetTutorialByIdQuery(tutorial_id=TutorialId(tutorial_id), user_id=user_id)

    def _when_handle_query(self, handler: GetTutorialByIdQueryHandler, query: GetTutorialByIdQuery) -> Tutorial | None:
        return handler.handle(query)

    def _then_tutorial_should_equal(self, actual: Tutorial | None, expected: Tutorial) -> None:
        assert actual == expected

    def _then_result_should_be_none(self, result: Tutorial | None) -> None:
        assert result is None

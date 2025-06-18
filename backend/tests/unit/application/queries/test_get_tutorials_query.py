from datetime import datetime, timedelta, timezone

from sightcall_transcript_to_tutorial.application.queries.get_tutorials_query import (
    GetTutorialsQuery,
    GetTutorialsQueryHandler,
)
from sightcall_transcript_to_tutorial.domain.entities import Tutorial
from sightcall_transcript_to_tutorial.domain.repositories import TutorialRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects import TutorialId, UserId
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_tutorial_repository import (
    FakeTutorialRepository,
)


class TestGetTutorialsQueryHandler:
    def test_should_list_tutorials_for_user(self):
        # Given
        repo = self._given_repository()
        user_id = UserId("user-1")
        self._given_tutorials_in_repository(repo, user_id, count=3)
        handler = self._given_handler(repo)
        query = self._given_query(user_id)

        # When
        result = self._when_handle_query(handler, query)

        # Then
        self._then_result_should_have_count(result, 3)

    def test_should_paginate_tutorials(self):
        # Given
        repo = self._given_repository()
        user_id = UserId("user-1")
        self._given_tutorials_in_repository(repo, user_id, count=5)
        handler = self._given_handler(repo)
        query = self._given_query(user_id, page=2, page_size=2)

        # When
        result = self._when_handle_query(handler, query)

        # Then
        self._then_result_should_have_count(result, 2)

    def test_should_search_tutorials_by_title(self):
        # Given
        repo = self._given_repository()
        user_id = UserId("user-1")
        self._given_tutorials_in_repository(repo, user_id, count=3, base_title="Special")
        handler = self._given_handler(repo)
        query = self._given_query(user_id, search="Special 1")

        # When
        result = self._when_handle_query(handler, query)

        # Then
        self._then_result_should_have_count(result, 1)
        self._then_first_tutorial_should_have_title(result, "Special 1")

    def test_should_filter_tutorials_by_created_at(self):
        # Given
        repo = self._given_repository()
        user_id = UserId("user-1")
        now = datetime.now(timezone.utc)
        self._given_tutorials_with_timestamps(repo, user_id, now)
        handler = self._given_handler(repo)
        filters = {"created_after": now - timedelta(days=1)}
        query = self._given_query(user_id, filters=filters)

        # When
        result = self._when_handle_query(handler, query)

        # Then
        self._then_all_tutorials_should_be_created_after(result, filters["created_after"])

    def _given_repository(self) -> FakeTutorialRepository:
        return FakeTutorialRepository()

    def _given_tutorials_in_repository(
        self, repo: TutorialRepositoryInterface, user_id: UserId, count: int = 3, base_title: str = "Title"
    ) -> None:
        now = datetime.now(timezone.utc)
        for i in range(count):
            tutorial = Tutorial(
                TutorialId(f"tut{i}"),
                title=f"{base_title} {i}",
                content="content",
                user_id=user_id,
                created_at=now - timedelta(days=i),
                updated_at=now - timedelta(days=i),
            )
            repo.save(tutorial)

    def _given_tutorials_with_timestamps(
        self, repo: TutorialRepositoryInterface, user_id: UserId, base_time: datetime
    ) -> None:
        for i in range(3):
            tutorial = Tutorial(
                TutorialId(f"tut{i}"),
                title=f"Title {i}",
                content="content",
                user_id=user_id,
                created_at=base_time - timedelta(days=i),
                updated_at=base_time - timedelta(days=i),
            )
            repo.save(tutorial)

    def _given_handler(self, repo: TutorialRepositoryInterface) -> GetTutorialsQueryHandler:
        return GetTutorialsQueryHandler(repo)

    def _given_query(
        self,
        user_id: UserId,
        page: int = 1,
        page_size: int = 10,
        search: str | None = None,
        filters: dict | None = None,
    ) -> GetTutorialsQuery:
        return GetTutorialsQuery(user_id=user_id, page=page, page_size=page_size, search=search, filters=filters)

    def _when_handle_query(self, handler: GetTutorialsQueryHandler, query: GetTutorialsQuery) -> list[Tutorial]:
        return handler.handle(query)

    def _then_result_should_have_count(self, result: list[Tutorial], expected_count: int) -> None:
        assert len(result) == expected_count

    def _then_first_tutorial_should_have_title(self, result: list[Tutorial], expected_title: str) -> None:
        assert len(result) > 0
        assert result[0].title == expected_title

    def _then_all_tutorials_should_be_created_after(self, result: list[Tutorial], threshold: datetime) -> None:
        assert all(tutorial.created_at > threshold for tutorial in result)

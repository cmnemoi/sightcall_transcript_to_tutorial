import pytest

from sightcall_transcript_to_tutorial.domain.entities import Tutorial
from sightcall_transcript_to_tutorial.domain.value_objects import TutorialId, UserId
from sightcall_transcript_to_tutorial.infrastructure.for_production.repositories.sqlalchemy_tutorial_repository import (
    SQLAlchemyTutorialRepository,
)


class TestSQLAlchemyTutorialRepository:
    @pytest.mark.integration
    def test_should_save_and_find_tutorial_by_id(self, pg_session):
        """Given a tutorial, when saved and fetched by id, then it should be equal."""
        # Given
        repo = self._given_repository(pg_session)
        tutorial = self._given_tutorial_in_repository(repo, "tut1", UserId("user-1"))

        # When
        fetched_tutorial = self._when_find_by_id(repo, "tut1")

        # Then
        self._then_tutorial_should_equal(fetched_tutorial, tutorial)

    @pytest.mark.integration
    def test_should_delete_tutorial_successfully(self, pg_session):
        """Given a tutorial, when deleted, then it should not be found."""
        # Given
        repo = self._given_repository(pg_session)
        self._given_tutorial_in_repository(repo, "tut1", UserId("user-1"))

        # When
        self._when_delete_tutorial(repo, "tut1")

        # Then
        self._then_tutorial_should_not_be_found(repo, "tut1")

    @pytest.mark.integration
    def test_should_list_tutorials_with_pagination_and_search(self, pg_session):
        """Given multiple tutorials, when listing, then pagination and search should work."""
        # Given
        repo = self._given_repository(pg_session)
        user_1 = UserId("user-1")
        user_2 = UserId("user-2")
        self._given_multiple_tutorials_for_users(repo, user_1, user_2)

        # When & Then
        self._when_list_tutorials_then_should_return_user_tutorials(repo, user_1)
        self._when_paginate_tutorials_then_should_return_correct_pages(repo, user_1)
        self._when_search_tutorials_then_should_return_matching_results(repo, user_1)

    @pytest.mark.integration
    def test_should_update_tutorial_for_owner_only(self, pg_session):
        """Given a tutorial, when updated by owner, then fields should change; non-owner cannot update."""
        # Given
        repo = self._given_repository(pg_session)
        user_id = UserId("user-1")
        self._given_tutorial_in_repository(repo, "tut1", user_id, title="Old Title", content="Old content")

        # When & Then
        self._when_update_as_owner_then_should_succeed(repo, user_id)
        self._when_update_as_non_owner_then_should_fail(repo)

    @pytest.mark.integration
    def test_should_validate_ownership_correctly(self, pg_session):
        """Given a tutorial, when validating ownership, then only the owner is valid."""
        # Given
        repo = self._given_repository(pg_session)
        user_id = UserId("user-1")
        self._given_tutorial_in_repository(repo, "tut1", user_id)

        # When
        is_owner = self._when_validate_ownership(repo, "tut1", user_id)
        is_not_owner = self._when_validate_ownership(repo, "tut1", UserId("other-user"))

        # Then
        self._then_ownership_should_be_valid(is_owner, True)
        self._then_ownership_should_be_valid(is_not_owner, False)

    def _given_repository(self, pg_session) -> SQLAlchemyTutorialRepository:
        return SQLAlchemyTutorialRepository(pg_session)

    def _given_tutorial_in_repository(
        self,
        repo: SQLAlchemyTutorialRepository,
        tutorial_id: str,
        user_id: UserId,
        title: str = "How to use",
        content: str = "sample content",
    ) -> Tutorial:
        tutorial = Tutorial(TutorialId(tutorial_id), title=title, content=content, user_id=user_id)
        repo.save(tutorial)
        return tutorial

    def _given_multiple_tutorials_for_users(
        self, repo: SQLAlchemyTutorialRepository, user_1: UserId, user_2: UserId
    ) -> None:
        # Create tutorials for user1
        for i in range(3):
            self._given_tutorial_in_repository(repo, f"tut{i}", user_1, title=f"Title {i}")

        # Create tutorials for user2
        for i in range(2):
            self._given_tutorial_in_repository(repo, f"tutX{i}", user_2, title=f"Other {i}")

    def _when_find_by_id(self, repo: SQLAlchemyTutorialRepository, tutorial_id: str) -> Tutorial | None:
        return repo.find_by_id(TutorialId(tutorial_id))

    def _when_delete_tutorial(self, repo: SQLAlchemyTutorialRepository, tutorial_id: str) -> None:
        repo.delete(TutorialId(tutorial_id))

    def _when_list_tutorials_then_should_return_user_tutorials(
        self, repo: SQLAlchemyTutorialRepository, user_id: UserId
    ) -> None:
        result = repo.list_tutorials(user_id=user_id)
        assert len(result) == 3

    def _when_paginate_tutorials_then_should_return_correct_pages(
        self, repo: SQLAlchemyTutorialRepository, user_id: UserId
    ) -> None:
        result_page_1 = repo.list_tutorials(user_id=user_id, page=1, page_size=2)
        result_page_2 = repo.list_tutorials(user_id=user_id, page=2, page_size=2)
        assert len(result_page_1) == 2
        assert len(result_page_2) == 1

    def _when_search_tutorials_then_should_return_matching_results(
        self, repo: SQLAlchemyTutorialRepository, user_id: UserId
    ) -> None:
        result_search = repo.list_tutorials(user_id=user_id, search="Title 1")
        assert len(result_search) == 1
        assert result_search[0].title == "Title 1"

    def _when_update_as_owner_then_should_succeed(self, repo: SQLAlchemyTutorialRepository, user_id: UserId) -> None:
        updated_tutorial = repo.update_tutorial(
            tutorial_id=TutorialId("tut1"), user_id=user_id, title="New Title", content="New content"
        )
        assert updated_tutorial is not None
        assert updated_tutorial.title == "New Title"
        assert updated_tutorial.content == "New content"

    def _when_update_as_non_owner_then_should_fail(self, repo: SQLAlchemyTutorialRepository) -> None:
        updated_tutorial = repo.update_tutorial(
            tutorial_id=TutorialId("tut1"), user_id=UserId("other-user"), title="X"
        )
        assert updated_tutorial is None

    def _when_validate_ownership(self, repo: SQLAlchemyTutorialRepository, tutorial_id: str, user_id: UserId) -> bool:
        return repo.validate_ownership(TutorialId(tutorial_id), user_id)

    def _then_tutorial_should_equal(self, actual: Tutorial | None, expected: Tutorial) -> None:
        assert actual == expected

    def _then_tutorial_should_not_be_found(self, repo: SQLAlchemyTutorialRepository, tutorial_id: str) -> None:
        tutorial = repo.find_by_id(TutorialId(tutorial_id))
        assert tutorial is None

    def _then_ownership_should_be_valid(self, actual: bool, expected: bool) -> None:
        assert actual == expected

from sightcall_transcript_to_tutorial.domain.entities import Tutorial
from sightcall_transcript_to_tutorial.domain.value_objects import TutorialId, UserId
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_tutorial_repository import (
    FakeTutorialRepository,
)


class TestFakeTutorialRepository:
    def test_should_save_and_find_tutorial_by_id(self):
        # Given
        repo = self._given_repository()
        tutorial = self._given_tutorial("tut1", "How to use", "sample content", "user-1")

        # When
        self._when_save_tutorial(repo, tutorial)
        found_tutorial = self._when_find_by_id(repo, "tut1")

        # Then
        self._then_tutorial_should_equal(found_tutorial, tutorial)

    def test_should_return_none_when_tutorial_not_found(self):
        # Given
        repo = self._given_repository()

        # When
        found_tutorial = self._when_find_by_id(repo, "missing")

        # Then
        self._then_tutorial_should_be_none(found_tutorial)

    def test_should_delete_tutorial_successfully(self):
        # Given
        repo = self._given_repository()
        tutorial = self._given_tutorial("tut1", "How to use", "sample content", "user-1")
        self._when_save_tutorial(repo, tutorial)

        # When
        self._when_delete_tutorial(repo, "tut1")
        found_tutorial = self._when_find_by_id(repo, "tut1")

        # Then
        self._then_tutorial_should_be_none(found_tutorial)

    def test_should_handle_delete_nonexistent_tutorial_gracefully(self):
        # Given
        repo = self._given_repository()

        # When & Then (should not raise exception)
        self._when_delete_tutorial(repo, "doesnotexist")

    def test_should_list_tutorials_by_user(self):
        # Given
        repo = self._given_repository()
        user_1 = UserId("user-1")
        tutorial_1 = self._given_tutorial("tut1", "A", "C1", "user-1")
        tutorial_2 = self._given_tutorial("tut2", "B", "C2", "user-1")
        tutorial_3 = self._given_tutorial("tut3", "C", "C3", "user-2")
        self._when_save_tutorials(repo, [tutorial_1, tutorial_2, tutorial_3])

        # When
        result = self._when_list_tutorials_by_user(repo, user_1)

        # Then
        self._then_result_should_contain_tutorial_ids(result, {"tut1", "tut2"})

    def test_should_search_tutorials_by_title(self):
        # Given
        repo = self._given_repository()
        user_id = UserId("user-1")
        tutorial_1 = self._given_tutorial("tut1", "Python Basics", "C1", "user-1")
        tutorial_2 = self._given_tutorial("tut2", "Advanced Python", "C2", "user-1")
        tutorial_3 = self._given_tutorial("tut3", "JavaScript", "C3", "user-1")
        self._when_save_tutorials(repo, [tutorial_1, tutorial_2, tutorial_3])

        # When
        result = self._when_list_tutorials_with_search(repo, user_id, "python")

        # Then
        self._then_result_should_contain_tutorial_ids(result, {"tut1", "tut2"})

    def test_should_paginate_tutorials(self):
        # Given
        repo = self._given_repository()
        user_id = UserId("user-1")
        tutorials = [self._given_tutorial(f"tut{i}", f"T{i}", "C", "user-1") for i in range(1, 11)]
        self._when_save_tutorials(repo, tutorials)

        # When
        page_1 = self._when_list_tutorials_with_pagination(repo, user_id, page=1, page_size=3)
        page_2 = self._when_list_tutorials_with_pagination(repo, user_id, page=2, page_size=3)

        # Then
        self._then_result_should_have_count(page_1, 3)
        self._then_result_should_have_count(page_2, 3)
        self._then_results_should_be_different(page_1, page_2)

    def test_should_update_tutorial_for_owner(self):
        # Given
        repo = self._given_repository()
        user_id = UserId("user-1")
        tutorial = self._given_tutorial("tut1", "Old", "Old", "user-1")
        self._when_save_tutorial(repo, tutorial)

        # When
        updated_tutorial = self._when_update_tutorial(repo, "tut1", user_id, "New Title", "New Content")

        # Then
        self._then_tutorial_should_be_updated(updated_tutorial, "New Title", "New Content", tutorial.tutorial_id)

    def test_should_return_none_when_updating_tutorial_with_wrong_user(self):
        # Given
        repo = self._given_repository()
        other_user_id = UserId("user-2")
        tutorial = self._given_tutorial("tut1", "Old", "Old", "user-1")
        self._when_save_tutorial(repo, tutorial)

        # When
        result = self._when_update_tutorial(repo, "tut1", other_user_id, "X")

        # Then
        self._then_tutorial_should_be_none(result)

    def test_should_validate_ownership_correctly(self):
        # Given
        repo = self._given_repository()
        user_id = UserId("user-1")
        tutorial = self._given_tutorial("tut1", "T", "C", "user-1")
        self._when_save_tutorial(repo, tutorial)

        # When
        is_owner = self._when_validate_ownership(repo, "tut1", user_id)
        is_not_owner = self._when_validate_ownership(repo, "tut1", UserId("user-2"))

        # Then
        self._then_ownership_should_be_valid(is_owner, True)
        self._then_ownership_should_be_valid(is_not_owner, False)

    def _given_repository(self) -> FakeTutorialRepository:
        return FakeTutorialRepository()

    def _given_tutorial(self, tutorial_id: str, title: str, content: str, user_id: str) -> Tutorial:
        return Tutorial(TutorialId(tutorial_id), title=title, content=content, user_id=UserId(user_id))

    def _when_save_tutorial(self, repo: FakeTutorialRepository, tutorial: Tutorial) -> None:
        repo.save(tutorial)

    def _when_save_tutorials(self, repo: FakeTutorialRepository, tutorials: list[Tutorial]) -> None:
        for tutorial in tutorials:
            repo.save(tutorial)

    def _when_find_by_id(self, repo: FakeTutorialRepository, tutorial_id: str) -> Tutorial | None:
        return repo.find_by_id(TutorialId(tutorial_id))

    def _when_delete_tutorial(self, repo: FakeTutorialRepository, tutorial_id: str) -> None:
        repo.delete(TutorialId(tutorial_id))

    def _when_list_tutorials_by_user(self, repo: FakeTutorialRepository, user_id: UserId) -> list[Tutorial]:
        return repo.list_tutorials(user_id=user_id)

    def _when_list_tutorials_with_search(
        self, repo: FakeTutorialRepository, user_id: UserId, search: str
    ) -> list[Tutorial]:
        return repo.list_tutorials(user_id=user_id, search=search)

    def _when_list_tutorials_with_pagination(
        self, repo: FakeTutorialRepository, user_id: UserId, page: int, page_size: int
    ) -> list[Tutorial]:
        return repo.list_tutorials(user_id=user_id, page=page, page_size=page_size)

    def _when_update_tutorial(
        self, repo: FakeTutorialRepository, tutorial_id: str, user_id: UserId, title: str, content: str | None = None
    ) -> Tutorial | None:
        return repo.update_tutorial(tutorial_id=TutorialId(tutorial_id), user_id=user_id, title=title, content=content)

    def _when_validate_ownership(self, repo: FakeTutorialRepository, tutorial_id: str, user_id: UserId) -> bool:
        return repo.validate_ownership(TutorialId(tutorial_id), user_id)

    def _then_tutorial_should_equal(self, actual: Tutorial | None, expected: Tutorial) -> None:
        assert actual == expected

    def _then_tutorial_should_be_none(self, tutorial: Tutorial | None) -> None:
        assert tutorial is None

    def _then_result_should_contain_tutorial_ids(self, result: list[Tutorial], expected_ids: set[str]) -> None:
        actual_ids = {tutorial.tutorial_id.value for tutorial in result}
        assert actual_ids == expected_ids

    def _then_result_should_have_count(self, result: list[Tutorial], expected_count: int) -> None:
        assert len(result) == expected_count

    def _then_results_should_be_different(self, result_1: list[Tutorial], result_2: list[Tutorial]) -> None:
        assert result_1 != result_2

    def _then_tutorial_should_be_updated(
        self, tutorial: Tutorial | None, expected_title: str, expected_content: str, expected_id: TutorialId
    ) -> None:
        assert tutorial is not None
        assert tutorial.title == expected_title
        assert tutorial.content == expected_content
        assert tutorial.tutorial_id == expected_id

    def _then_ownership_should_be_valid(self, actual: bool, expected: bool) -> None:
        assert actual == expected

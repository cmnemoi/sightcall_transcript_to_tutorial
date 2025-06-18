import datetime

import pytest

from sightcall_transcript_to_tutorial.domain.entities import Tutorial
from sightcall_transcript_to_tutorial.domain.exceptions.tutorial_generation_error import TutorialGenerationError
from sightcall_transcript_to_tutorial.domain.value_objects import TutorialId, UserId


class TestTutorial:
    def test_should_create_tutorial_with_valid_properties(self):
        # Given
        tutorial_id = TutorialId("tut1")
        title = "How to use"
        content = "sample content"
        user_id = UserId("user-1")

        # When
        tutorial = self._when_create_tutorial(tutorial_id, title, content, user_id)

        # Then
        self._then_tutorial_should_have_properties(tutorial, tutorial_id, title)

    def test_should_be_equal_when_same_properties(self):
        # Given
        now = datetime.datetime(2023, 1, 1, 12, 0, 0)
        tutorial_1 = self._given_tutorial_with_timestamps("tut1", "A", "sample content", "user-1", now)
        tutorial_2 = self._given_tutorial_with_timestamps("tut1", "A", "sample content", "user-1", now)
        tutorial_3 = self._given_tutorial_with_timestamps("tut2", "A", "sample content", "user-1", now)

        # When & Then
        self._then_tutorials_should_be_equal(tutorial_1, tutorial_2)
        self._then_tutorials_should_not_be_equal(tutorial_1, tutorial_3)

    def test_should_raise_error_when_title_is_empty(self):
        # Given
        tutorial_id = TutorialId("tut1")
        empty_title = ""
        content = "sample content"
        user_id = UserId("user-1")

        # When & Then
        with pytest.raises(ValueError):
            self._when_create_tutorial(tutorial_id, empty_title, content, user_id)

    def test_should_set_and_get_content(self):
        # Given
        content = "AI generated content"
        tutorial = self._given_tutorial_with_content(content)

        # When & Then
        self._then_tutorial_should_have_content(tutorial, content)

    def test_should_raise_error_when_content_is_empty(self):
        # Given
        tutorial_id = TutorialId("tut1")
        title = "How to use"
        empty_content = ""
        user_id = UserId("user-1")

        # When & Then
        with pytest.raises(ValueError):
            self._when_create_tutorial(tutorial_id, title, empty_content, user_id)

    def test_should_raise_tutorial_generation_error(self):
        # When & Then
        with pytest.raises(TutorialGenerationError):
            raise TutorialGenerationError("AI failed")

    def test_should_create_tutorial_with_user_ownership(self):
        # Given
        user_id = UserId("user-1")
        tutorial = self._given_tutorial_with_user(user_id)

        # When & Then
        self._then_tutorial_should_belong_to_user(tutorial, user_id)

    def test_should_create_tutorial_with_timestamps(self):
        # Given
        now = datetime.datetime.now(datetime.timezone.utc)
        tutorial = self._given_tutorial_with_timestamps("tut1", "How to use", "sample content", "user-1", now)

        # When & Then
        self._then_tutorial_should_have_timestamps(tutorial, now, now)

    def test_should_update_title_and_content(self):
        # Given
        tutorial = self._given_tutorial()
        new_title = "New Title"
        new_content = "New content"

        # When
        self._when_update_tutorial(tutorial, new_title, new_content)

        # Then
        self._then_tutorial_should_have_title_and_content(tutorial, new_title, new_content)

    def test_should_validate_title_and_content_on_update(self):
        # Given
        tutorial = self._given_tutorial()

        # When & Then
        with pytest.raises(ValueError):
            tutorial.update_title("")
        with pytest.raises(ValueError):
            tutorial.update_content("")

    def test_should_update_updated_at_timestamp_on_update(self):
        # Given
        now = datetime.datetime.now(datetime.timezone.utc)
        tutorial = self._given_tutorial_with_timestamps("tut1", "Old Title", "Old content", "user-1", now)
        later = now + datetime.timedelta(minutes=5)

        # When
        tutorial.update_title("New Title", updated_at=later)

        # Then
        self._then_tutorial_should_have_updated_at(tutorial, later)

    def _given_tutorial(self) -> Tutorial:
        return Tutorial(TutorialId("tut1"), title="Old Title", content="Old content", user_id=UserId("user-1"))

    def _given_tutorial_with_content(self, content: str) -> Tutorial:
        return Tutorial(TutorialId("tut1"), title="How to use", content=content, user_id=UserId("user-1"))

    def _given_tutorial_with_user(self, user_id: UserId) -> Tutorial:
        return Tutorial(TutorialId("tut1"), title="How to use", content="sample content", user_id=user_id)

    def _given_tutorial_with_timestamps(
        self, tutorial_id: str, title: str, content: str, user_id: str, timestamp: datetime.datetime
    ) -> Tutorial:
        return Tutorial(
            TutorialId(tutorial_id),
            title=title,
            content=content,
            user_id=UserId(user_id),
            created_at=timestamp,
            updated_at=timestamp,
        )

    def _when_create_tutorial(self, tutorial_id: TutorialId, title: str, content: str, user_id: UserId) -> Tutorial:
        return Tutorial(tutorial_id, title=title, content=content, user_id=user_id)

    def _when_update_tutorial(self, tutorial: Tutorial, title: str, content: str) -> None:
        tutorial.update_title(title)
        tutorial.update_content(content)

    def _then_tutorial_should_have_properties(
        self, tutorial: Tutorial, expected_id: TutorialId, expected_title: str
    ) -> None:
        assert tutorial.tutorial_id == expected_id
        assert tutorial.title == expected_title

    def _then_tutorials_should_be_equal(self, tutorial_1: Tutorial, tutorial_2: Tutorial) -> None:
        assert tutorial_1 == tutorial_2

    def _then_tutorials_should_not_be_equal(self, tutorial_1: Tutorial, tutorial_2: Tutorial) -> None:
        assert tutorial_1 != tutorial_2

    def _then_tutorial_should_have_content(self, tutorial: Tutorial, expected_content: str) -> None:
        assert tutorial.content == expected_content

    def _then_tutorial_should_belong_to_user(self, tutorial: Tutorial, expected_user_id: UserId) -> None:
        assert tutorial.user_id == expected_user_id

    def _then_tutorial_should_have_timestamps(
        self, tutorial: Tutorial, expected_created_at: datetime.datetime, expected_updated_at: datetime.datetime
    ) -> None:
        assert tutorial.created_at == expected_created_at
        assert tutorial.updated_at == expected_updated_at

    def _then_tutorial_should_have_title_and_content(
        self, tutorial: Tutorial, expected_title: str, expected_content: str
    ) -> None:
        assert tutorial.title == expected_title
        assert tutorial.content == expected_content

    def _then_tutorial_should_have_updated_at(
        self, tutorial: Tutorial, expected_updated_at: datetime.datetime
    ) -> None:
        assert tutorial.updated_at == expected_updated_at

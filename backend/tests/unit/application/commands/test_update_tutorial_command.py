from datetime import datetime, timezone

from sightcall_transcript_to_tutorial.application.commands.update_tutorial_command import (
    UpdateTutorialCommand,
    UpdateTutorialCommandHandler,
)
from sightcall_transcript_to_tutorial.domain.entities import Tutorial
from sightcall_transcript_to_tutorial.domain.value_objects import TutorialId, UserId
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_tutorial_repository import (
    FakeTutorialRepository,
)


class TestUpdateTutorialCommandHandler:
    def test_should_update_tutorial_when_user_is_owner(self):
        # Given
        repo = self._given_repository()
        user_id = UserId("user-1")
        self._given_tutorial_in_repository(repo, "tut1", user_id)
        handler = self._given_handler(repo)
        command = self._given_update_command("tut1", user_id, title="New Title", content="New Content")

        # When
        updated_tutorial = self._when_handle_command(handler, command)

        # Then
        self._then_tutorial_should_be_updated(updated_tutorial, "New Title", "New Content", user_id)

    def test_should_return_none_when_user_is_not_owner(self):
        # Given
        repo = self._given_repository()
        owner_user_id = UserId("user-1")
        non_owner_user_id = UserId("other-user")
        self._given_tutorial_in_repository(repo, "tut1", owner_user_id)
        handler = self._given_handler(repo)
        command = self._given_update_command("tut1", non_owner_user_id, title="New Title")

        # When
        updated_tutorial = self._when_handle_command(handler, command)

        # Then
        self._then_tutorial_should_be_none(updated_tutorial)

    def test_should_return_none_when_tutorial_not_found(self):
        # Given
        repo = self._given_repository()
        handler = self._given_handler(repo)
        command = self._given_update_command("non-existent", UserId("user-1"), title="New Title")

        # When
        updated_tutorial = self._when_handle_command(handler, command)

        # Then
        self._then_tutorial_should_be_none(updated_tutorial)

    def test_should_update_only_title_when_content_not_provided(self):
        # Given
        repo = self._given_repository()
        user_id = UserId("user-1")
        self._given_tutorial_in_repository(repo, "tut1", user_id, title="Old Title", content="Old Content")
        handler = self._given_handler(repo)
        command = self._given_update_command("tut1", user_id, title="New Title")

        # When
        updated_tutorial = self._when_handle_command(handler, command)

        # Then
        self._then_tutorial_should_be_updated(updated_tutorial, "New Title", "Old Content", user_id)

    def test_should_update_only_content_when_title_not_provided(self):
        # Given
        repo = self._given_repository()
        user_id = UserId("user-1")
        self._given_tutorial_in_repository(repo, "tut1", user_id, title="Old Title", content="Old Content")
        handler = self._given_handler(repo)
        command = self._given_update_command("tut1", user_id, content="New Content")

        # When
        updated_tutorial = self._when_handle_command(handler, command)

        # Then
        self._then_tutorial_should_be_updated(updated_tutorial, "Old Title", "New Content", user_id)

    def _given_repository(self) -> FakeTutorialRepository:
        return FakeTutorialRepository()

    def _given_tutorial_in_repository(
        self,
        repo: FakeTutorialRepository,
        tutorial_id: str,
        user_id: UserId,
        title: str = "Old Title",
        content: str = "Old Content",
    ) -> Tutorial:
        now = datetime.now(timezone.utc)
        tutorial = Tutorial(
            tutorial_id=TutorialId(tutorial_id),
            title=title,
            content=content,
            user_id=user_id,
            created_at=now,
            updated_at=now,
        )
        repo.save(tutorial)
        return tutorial

    def _given_handler(self, repo: FakeTutorialRepository) -> UpdateTutorialCommandHandler:
        return UpdateTutorialCommandHandler(repo)

    def _given_update_command(
        self, tutorial_id: str, user_id: UserId, title: str | None = None, content: str | None = None
    ) -> UpdateTutorialCommand:
        return UpdateTutorialCommand(
            tutorial_id=TutorialId(tutorial_id), user_id=user_id, title=title, content=content
        )

    def _when_handle_command(
        self, handler: UpdateTutorialCommandHandler, command: UpdateTutorialCommand
    ) -> Tutorial | None:
        return handler.handle(command)

    def _then_tutorial_should_be_updated(
        self, tutorial: Tutorial | None, expected_title: str, expected_content: str, expected_user_id: UserId
    ) -> None:
        assert tutorial is not None
        assert tutorial.title == expected_title
        assert tutorial.content == expected_content
        assert tutorial.user_id == expected_user_id

    def _then_tutorial_should_be_none(self, tutorial: Tutorial | None) -> None:
        assert tutorial is None

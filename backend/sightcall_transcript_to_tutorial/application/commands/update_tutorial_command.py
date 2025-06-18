from typing import Optional

from sightcall_transcript_to_tutorial.domain.entities import Tutorial
from sightcall_transcript_to_tutorial.domain.repositories import TutorialRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects import TutorialId, UserId


class UpdateTutorialCommand:
    def __init__(
        self, tutorial_id: TutorialId, user_id: UserId, title: Optional[str] = None, content: Optional[str] = None
    ):
        self.tutorial_id = tutorial_id
        self.user_id = user_id
        self.title = title
        self.content = content


class UpdateTutorialCommandHandler:
    def __init__(self, tutorial_repository: TutorialRepositoryInterface):
        self._tutorial_repository = tutorial_repository

    def handle(self, command: UpdateTutorialCommand) -> Optional[Tutorial]:
        return self._tutorial_repository.update_tutorial(
            tutorial_id=command.tutorial_id,
            user_id=command.user_id,
            title=command.title,
            content=command.content,
        )

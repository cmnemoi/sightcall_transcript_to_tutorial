from typing import Optional

from sightcall_transcript_to_tutorial.domain.entities import Tutorial
from sightcall_transcript_to_tutorial.domain.repositories import TutorialRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects import TutorialId, UserId


class GetTutorialByIdQuery:
    def __init__(self, tutorial_id: TutorialId, user_id: UserId):
        self.tutorial_id = tutorial_id
        self.user_id = user_id


class GetTutorialByIdQueryHandler:
    def __init__(self, tutorial_repository: TutorialRepositoryInterface):
        self._tutorial_repository = tutorial_repository

    def handle(self, query: GetTutorialByIdQuery) -> Optional[Tutorial]:
        tutorial = self._tutorial_repository.find_by_id(query.tutorial_id)
        if not tutorial or tutorial.user_id != query.user_id:
            return None
        return tutorial

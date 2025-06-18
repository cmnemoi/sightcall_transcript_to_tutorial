from typing import Any, List, Optional

from sightcall_transcript_to_tutorial.domain.entities import Tutorial
from sightcall_transcript_to_tutorial.domain.repositories import TutorialRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects import UserId


class GetTutorialsQuery:
    def __init__(
        self,
        user_id: UserId,
        filters: Optional[dict[str, Any]] = None,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
    ):
        self.user_id = user_id
        self.filters = filters
        self.page = page
        self.page_size = page_size
        self.search = search


class GetTutorialsQueryHandler:
    def __init__(self, tutorial_repository: TutorialRepositoryInterface):
        self._tutorial_repository = tutorial_repository

    def handle(self, query: GetTutorialsQuery) -> List[Tutorial]:
        return self._tutorial_repository.list_tutorials(
            user_id=query.user_id,
            filters=query.filters,
            page=query.page,
            page_size=query.page_size,
            search=query.search,
        )

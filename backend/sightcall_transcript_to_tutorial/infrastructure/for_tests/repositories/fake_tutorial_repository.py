from typing import Any, Optional

from sightcall_transcript_to_tutorial.domain.entities import Tutorial
from sightcall_transcript_to_tutorial.domain.repositories import TutorialRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects import TutorialId, UserId


class FakeTutorialRepository(TutorialRepositoryInterface):
    def __init__(self):
        self._tutorials: dict[str, Tutorial] = {}

    def find_by_id(self, tutorial_id: TutorialId) -> Tutorial | None:
        return self._tutorials.get(tutorial_id.value)

    def save(self, tutorial: Tutorial) -> None:
        self._tutorials[tutorial.tutorial_id.value] = tutorial

    def delete(self, tutorial_id: TutorialId) -> None:
        self._tutorials.pop(tutorial_id.value, None)

    def list_tutorials(
        self,
        user_id: UserId,
        filters: Optional[dict[str, Any]] = None,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
    ) -> list[Tutorial]:
        # Filter by user
        tutorials = [t for t in self._tutorials.values() if t.user_id == user_id]
        # Search by title (case-insensitive)
        if search:
            search_lower = search.lower()
            tutorials = [t for t in tutorials if search_lower in t.title.lower()]
        # Apply filters (e.g., created_at)
        if filters:
            for key, value in filters.items():
                if key == "created_after":
                    tutorials = [t for t in tutorials if t.created_at > value]
                if key == "created_before":
                    tutorials = [t for t in tutorials if t.created_at < value]
        # Pagination
        start = (page - 1) * page_size
        end = start + page_size
        return tutorials[start:end]

    def update_tutorial(
        self,
        tutorial_id: TutorialId,
        user_id: UserId,
        title: Optional[str] = None,
        content: Optional[str] = None,
        updated_at: Any = None,
    ) -> Tutorial | None:
        tutorial = self.find_by_id(tutorial_id)
        if not tutorial or tutorial.user_id != user_id:
            return None
        # Create a new Tutorial with updated fields (immutability)
        new_title = title if title is not None else tutorial.title
        new_content = content if content is not None else tutorial.content
        new_updated_at = updated_at
        if new_updated_at is None:
            import datetime

            new_updated_at = datetime.datetime.now(datetime.timezone.utc)
        updated_tutorial = Tutorial(
            tutorial_id=tutorial.tutorial_id,
            title=new_title,
            content=new_content,
            user_id=tutorial.user_id,
            created_at=tutorial.created_at,
            updated_at=new_updated_at,
        )
        self.save(updated_tutorial)
        return updated_tutorial

    def validate_ownership(self, tutorial_id: TutorialId, user_id: UserId) -> bool:
        tutorial = self.find_by_id(tutorial_id)
        return tutorial is not None and tutorial.user_id == user_id

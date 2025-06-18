from abc import ABC, abstractmethod
from typing import Any, Optional

from sightcall_transcript_to_tutorial.domain.entities import Tutorial
from sightcall_transcript_to_tutorial.domain.value_objects import TutorialId, UserId


class TutorialRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, tutorial_id: TutorialId) -> Tutorial | None:
        """Find a tutorial by its ID."""
        pass

    @abstractmethod
    def save(self, tutorial: Tutorial) -> None:
        """Save or update a tutorial."""
        pass

    @abstractmethod
    def delete(self, tutorial_id: TutorialId) -> None:
        """Delete a tutorial by its ID."""
        pass

    @abstractmethod
    def list_tutorials(
        self,
        user_id: UserId,
        filters: Optional[dict[str, Any]] = None,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
    ) -> list[Tutorial]:
        """
        List tutorials for a user, with optional filters (date, etc), pagination, and search by title.
        """
        pass

    @abstractmethod
    def update_tutorial(
        self,
        tutorial_id: TutorialId,
        user_id: UserId,
        title: Optional[str] = None,
        content: Optional[str] = None,
        updated_at: Any = None,
    ) -> Tutorial | None:
        """
        Update a tutorial's title/content (partial update). Returns updated tutorial or None if not found/owned.
        """
        pass

    @abstractmethod
    def validate_ownership(self, tutorial_id: TutorialId, user_id: UserId) -> bool:
        """
        Return True if the tutorial belongs to the user, else False.
        """
        pass

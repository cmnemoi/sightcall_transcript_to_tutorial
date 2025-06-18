from datetime import datetime, timezone
from typing import Any

from sightcall_transcript_to_tutorial.domain.value_objects.tutorial_id import TutorialId
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId


class Tutorial:
    def __init__(
        self,
        tutorial_id: TutorialId,
        title: str,
        content: str,
        user_id: UserId,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        if not title or not isinstance(title, str):
            raise ValueError("Tutorial title must be a non-empty string")
        if not content or not isinstance(content, str):
            raise ValueError("Tutorial content must be a non-empty string")
        if not isinstance(user_id, UserId):
            raise ValueError("user_id must be a UserId instance")
        now = datetime.now(timezone.utc)
        self._tutorial_id = tutorial_id
        self._title = title
        self._content = content
        self._user_id = user_id
        self._created_at = created_at or now
        self._updated_at = updated_at or now

    @property
    def tutorial_id(self) -> TutorialId:
        return self._tutorial_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def content(self) -> str:
        return self._content

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def update_title(self, new_title: str, updated_at: datetime | None = None) -> None:
        if not new_title or not isinstance(new_title, str):
            raise ValueError("Tutorial title must be a non-empty string")
        self._title = new_title
        self._updated_at = updated_at or datetime.now(timezone.utc)

    def update_content(self, new_content: str, updated_at: datetime | None = None) -> None:
        if not new_content or not isinstance(new_content, str):
            raise ValueError("Tutorial content must be a non-empty string")
        self._content = new_content
        self._updated_at = updated_at or datetime.now(timezone.utc)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Tutorial):
            return False
        return (
            self.tutorial_id == other.tutorial_id
            and self.title == other.title
            and self.content == other.content
            and self.user_id == other.user_id
            and self.created_at == other.created_at
            and self.updated_at == other.updated_at
        )

    def __repr__(self) -> str:
        return (
            f"Tutorial(tutorial_id={self.tutorial_id}, title={self.title}, content={self.content}, "
            f"user_id={self.user_id}, created_at={self.created_at}, updated_at={self.updated_at})"
        )

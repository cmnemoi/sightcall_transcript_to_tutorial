from abc import ABC, abstractmethod

from sightcall_transcript_to_tutorial.domain.entities import User
from sightcall_transcript_to_tutorial.domain.value_objects import UserId


class UserRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, user_id: UserId) -> User | None:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def delete(self, user_id: UserId) -> None:
        pass

    @abstractmethod
    def find_by_github_id(self, github_id: int) -> User | None:
        pass

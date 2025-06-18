from sightcall_transcript_to_tutorial.domain.entities import User
from sightcall_transcript_to_tutorial.domain.repositories import UserRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects import UserId


class FakeUserRepository(UserRepositoryInterface):
    def __init__(self):
        self._users: dict[str, User] = {}

    def find_by_id(self, user_id: UserId) -> User | None:
        return self._users.get(user_id.value)

    def save(self, user: User) -> None:
        self._users[user.user_id.value] = user

    def delete(self, user_id: UserId) -> None:
        self._users.pop(user_id.value, None)

    def find_by_github_id(self, github_id: int) -> User | None:
        return next((user for user in self._users.values() if user.github_id == github_id), None)

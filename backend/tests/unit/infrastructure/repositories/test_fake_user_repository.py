from sightcall_transcript_to_tutorial.domain.entities import User
from sightcall_transcript_to_tutorial.domain.repositories.user_repository_interface import UserRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects import UserId


class TestFakeUserRepository:
    def test_save_and_find_by_id(self):
        repo = FakeUserRepository()
        user = User(UserId("u1"), name="Alice")
        repo.save(user)
        assert repo.find_by_id(UserId("u1")) == user

    def test_find_by_id_not_found(self):
        repo = FakeUserRepository()
        assert repo.find_by_id(UserId("missing")) is None

    def test_delete(self):
        repo = FakeUserRepository()
        user = User(UserId("u1"), name="Alice")
        repo.save(user)
        repo.delete(UserId("u1"))
        assert repo.find_by_id(UserId("u1")) is None

    def test_delete_nonexistent(self):
        repo = FakeUserRepository()
        # Should not raise
        repo.delete(UserId("doesnotexist"))


class FakeUserRepository(UserRepositoryInterface):
    def __init__(self):
        self._users = {}

    def find_by_id(self, user_id: UserId) -> User | None:
        return self._users.get(user_id.value)

    def save(self, user: User) -> None:
        self._users[user.user_id.value] = user

    def delete(self, user_id: UserId) -> None:
        self._users.pop(user_id.value, None)

    def find_by_github_id(self, github_id: int) -> User | None:
        for user in self._users.values():
            if user.github_id == github_id:
                return user
        return None

from sightcall_transcript_to_tutorial.domain.entities.authenticated_user import AuthenticatedUser
from sightcall_transcript_to_tutorial.domain.value_objects import UserId


class User:
    def __init__(self, user_id: UserId, name: str, github_id: int | None = None):
        if not name or not isinstance(name, str):
            raise ValueError("User name must be a non-empty string")
        self._user_id = user_id
        self._name = name
        self._github_id = github_id

    @staticmethod
    def from_authenticated_user(authenticated_user: AuthenticatedUser) -> "User":
        return User(
            user_id=UserId.generate(),
            name=authenticated_user.username,
            github_id=authenticated_user.github_id,
        )

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def github_id(self) -> int | None:
        return self._github_id

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, User)
            and self.user_id == other.user_id
            and self.name == other.name
            and self.github_id == other.github_id
        )

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id!r}, name={self.name!r}, github_id={self.github_id!r})"

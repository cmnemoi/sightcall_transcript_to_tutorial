import uuid

from .base_id import BaseId


class UserId(BaseId):
    _type_name = "UserId"

    def __init__(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("UserId must be a non-empty string")
        self._value = value

    @staticmethod
    def generate() -> "UserId":
        return UserId(str(uuid.uuid4()))

    def __eq__(self, other):
        return isinstance(other, UserId) and self.value == other.value

    def __repr__(self):
        return f"UserId({self.value!r})"

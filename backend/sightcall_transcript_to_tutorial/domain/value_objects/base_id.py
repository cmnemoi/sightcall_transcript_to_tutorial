class BaseId:
    _type_name = "BaseId"

    def __init__(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError(f"{self._type_name} must be a non-empty string")
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other):
        return type(self) is type(other) and self.value == other.value

    def __hash__(self):
        return hash((type(self), self.value))

    def __repr__(self):
        return f"{self._type_name}({self.value!r})"

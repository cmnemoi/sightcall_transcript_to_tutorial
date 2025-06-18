import uuid

from .base_id import BaseId


class TutorialId(BaseId):
    _type_name = "TutorialId"

    @staticmethod
    def generate() -> "TutorialId":
        return TutorialId(str(uuid.uuid4()))

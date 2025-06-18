import uuid

from .base_id import BaseId


class TranscriptId(BaseId):
    _type_name = "TranscriptId"

    @staticmethod
    def generate() -> "TranscriptId":
        return TranscriptId(str(uuid.uuid4()))

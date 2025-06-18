from pydantic import BaseModel


class TranscriptUploadResponse(BaseModel):
    id: str


class ErrorResponse(BaseModel):
    error: str

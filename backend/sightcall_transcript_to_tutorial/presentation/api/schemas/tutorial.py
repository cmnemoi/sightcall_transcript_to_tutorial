from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class GenerateTutorialRequest(BaseModel):
    transcript_id: str


class TutorialResponse(BaseModel):
    title: str
    content: str


class TutorialDetailResponse(BaseModel):
    id: str
    title: str
    content: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class TutorialListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[TutorialDetailResponse]


class TutorialUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    content: Optional[str] = Field(None, min_length=1)

    @field_validator("title", mode="before")
    def title_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Title must not be empty")
        return v

    @field_validator("content", mode="before")
    def content_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Content must not be empty")
        return v

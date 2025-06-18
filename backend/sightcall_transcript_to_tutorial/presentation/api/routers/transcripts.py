from http import HTTPStatus

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from sightcall_transcript_to_tutorial.application.commands.upload_transcript_command import (
    UploadTranscriptCommand,
    UploadTranscriptCommandHandler,
)
from sightcall_transcript_to_tutorial.domain.entities.user import User
from sightcall_transcript_to_tutorial.domain.exceptions.tutorial_generation_error import InvalidTranscriptError
from sightcall_transcript_to_tutorial.domain.repositories.transcript_repository_interface import (
    TranscriptRepositoryInterface,
)
from sightcall_transcript_to_tutorial.domain.value_objects.transcript_content import TranscriptContent
from sightcall_transcript_to_tutorial.presentation.api.dependencies import (
    get_current_user_from_request_state,
    get_transcript_repository,
)
from sightcall_transcript_to_tutorial.presentation.api.schemas.transcript import (
    ErrorResponse,
    TranscriptUploadResponse,
)

router = APIRouter(prefix="/transcripts", tags=["transcripts"])


@router.post(
    "",
    response_model=TranscriptUploadResponse,
    status_code=HTTPStatus.CREATED.value,
    responses={
        HTTPStatus.BAD_REQUEST.value: {"model": ErrorResponse},
        HTTPStatus.UNAUTHORIZED.value: {"model": ErrorResponse},
        HTTPStatus.UNPROCESSABLE_ENTITY.value: {"model": ErrorResponse},
    },
)
def upload_transcript(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user_from_request_state),
    repository: TranscriptRepositoryInterface = Depends(get_transcript_repository),
):
    if file.content_type != "application/json":
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, detail="File must be a JSON transcript.")
    try:
        content_bytes = file.file.read()
        content_str = content_bytes.decode()
        transcript_content = TranscriptContent(content_str)
    except InvalidTranscriptError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value, detail=str(e))
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, detail="Invalid file upload.")
    handler = UploadTranscriptCommandHandler(repository)
    command = UploadTranscriptCommand(user=user, content=transcript_content)
    try:
        transcript_id = handler.handle(command)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, detail=f"Failed to save transcript: {e}")
    return TranscriptUploadResponse(id=transcript_id.value)

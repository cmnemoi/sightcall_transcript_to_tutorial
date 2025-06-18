from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status

from sightcall_transcript_to_tutorial.application.commands.generate_tutorial_command import (
    GenerateTutorialCommand,
    GenerateTutorialCommandHandler,
)
from sightcall_transcript_to_tutorial.application.commands.update_tutorial_command import (
    UpdateTutorialCommand,
    UpdateTutorialCommandHandler,
)
from sightcall_transcript_to_tutorial.application.queries.get_tutorial_by_id_query import (
    GetTutorialByIdQuery,
    GetTutorialByIdQueryHandler,
)
from sightcall_transcript_to_tutorial.application.queries.get_tutorials_query import (
    GetTutorialsQuery,
    GetTutorialsQueryHandler,
)
from sightcall_transcript_to_tutorial.domain.entities.user import User
from sightcall_transcript_to_tutorial.domain.gateways.tutorial_generator_gateway_interface import (
    TutorialGeneratorGatewayInterface,
)
from sightcall_transcript_to_tutorial.domain.repositories.transcript_repository_interface import (
    TranscriptRepositoryInterface,
)
from sightcall_transcript_to_tutorial.domain.repositories.tutorial_repository_interface import (
    TutorialRepositoryInterface,
)
from sightcall_transcript_to_tutorial.domain.value_objects.tutorial_id import TutorialId
from sightcall_transcript_to_tutorial.presentation.api.dependencies import (
    get_current_user_from_request_state,
    get_transcript_repository,
    get_tutorial_generator_gateway,
    get_tutorial_repository,
)
from sightcall_transcript_to_tutorial.presentation.api.schemas.tutorial import (
    GenerateTutorialRequest,
    TutorialDetailResponse,
    TutorialListResponse,
    TutorialResponse,
    TutorialUpdateRequest,
)

router = APIRouter()


@router.post("/tutorials/generate", response_model=TutorialResponse)
def generate_tutorial_endpoint(
    payload: GenerateTutorialRequest,
    user: User = Depends(get_current_user_from_request_state),
    transcript_repository: TranscriptRepositoryInterface = Depends(get_transcript_repository),
    tutorial_generator_gateway: TutorialGeneratorGatewayInterface = Depends(get_tutorial_generator_gateway),
    tutorial_repository: TutorialRepositoryInterface = Depends(get_tutorial_repository),
):
    command = GenerateTutorialCommand(transcript_id=payload.transcript_id, user_id=user.user_id)
    generate_tutorial = GenerateTutorialCommandHandler(
        transcript_repository, tutorial_generator_gateway, tutorial_repository
    )
    try:
        tutorial = generate_tutorial.handle(command)
        return TutorialResponse(title=tutorial.title, content=tutorial.content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": str(e)})


@router.get("/tutorials", response_model=TutorialListResponse)
def list_tutorials_endpoint(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    created_from: datetime = Query(None),
    created_to: datetime = Query(None),
    user: User = Depends(get_current_user_from_request_state),
    tutorial_repository: TutorialRepositoryInterface = Depends(get_tutorial_repository),
):
    filters = {}
    if created_from:
        filters["created_after"] = created_from
    if created_to:
        filters["created_before"] = created_to
    query = GetTutorialsQuery(
        user_id=user.user_id,
        filters=filters or None,
        page=page,
        page_size=page_size,
        search=search,
    )
    handler = GetTutorialsQueryHandler(tutorial_repository)
    tutorials = handler.handle(query)
    total = len(tutorials)
    items = [
        TutorialDetailResponse(
            id=tutorial.tutorial_id.value,
            title=tutorial.title,
            content=tutorial.content,
            user_id=tutorial.user_id.value,
            created_at=tutorial.created_at,
            updated_at=tutorial.updated_at,
        )
        for tutorial in tutorials
    ]
    return TutorialListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=items,
    )


@router.get("/tutorials/{tutorial_id}", response_model=TutorialDetailResponse)
def get_tutorial_by_id_endpoint(
    tutorial_id: str,
    user: User = Depends(get_current_user_from_request_state),
    tutorial_repository: TutorialRepositoryInterface = Depends(get_tutorial_repository),
):
    query = GetTutorialByIdQuery(tutorial_id=TutorialId(tutorial_id), user_id=user.user_id)
    handler = GetTutorialByIdQueryHandler(tutorial_repository)
    tutorial = handler.handle(query)
    if not tutorial:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return TutorialDetailResponse(
        id=tutorial.tutorial_id.value,
        title=tutorial.title,
        content=tutorial.content,
        user_id=tutorial.user_id.value,
        created_at=tutorial.created_at,
        updated_at=tutorial.updated_at,
    )


@router.patch("/tutorials/{tutorial_id}", response_model=TutorialDetailResponse)
def update_tutorial_endpoint(
    tutorial_id: str,
    payload: TutorialUpdateRequest,
    user: User = Depends(get_current_user_from_request_state),
    tutorial_repository: TutorialRepositoryInterface = Depends(get_tutorial_repository),
):
    command = UpdateTutorialCommand(
        tutorial_id=TutorialId(tutorial_id),
        user_id=user.user_id,
        title=payload.title,
        content=payload.content,
    )
    handler = UpdateTutorialCommandHandler(tutorial_repository)
    updated = handler.handle(command)
    if not updated:
        raise HTTPException(status_code=404, detail="Tutorial not found or not owned by user")
    return TutorialDetailResponse(
        id=updated.tutorial_id.value,
        title=updated.title,
        content=updated.content,
        user_id=updated.user_id.value,
        created_at=updated.created_at,
        updated_at=updated.updated_at,
    )

import os

import pytest

from sightcall_transcript_to_tutorial.domain.entities.transcript import Transcript
from sightcall_transcript_to_tutorial.domain.value_objects.transcript_id import TranscriptId
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId
from sightcall_transcript_to_tutorial.infrastructure.for_production.gateways.openai_tutorial_generator_gateway import (
    OpenAITutorialGeneratorGateway,
)


@pytest.mark.integration
@pytest.mark.slow
def test_should_generate_tutorial_with_openai_success():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set in environment")
    gateway = OpenAITutorialGeneratorGateway()
    transcript = Transcript(TranscriptId("tr1"), "How to reset your password in the app.")
    user_id = UserId("test-user-123")
    tutorial = gateway.generate_tutorial(transcript, user_id)
    assert tutorial.content
    assert "password" in tutorial.content.lower()
    assert tutorial.user_id == user_id

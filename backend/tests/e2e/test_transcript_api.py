import io

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from sightcall_transcript_to_tutorial.domain.config.settings import settings
from sightcall_transcript_to_tutorial.domain.entities.user import User
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_transcript_repository import (
    FakeTranscriptRepository,
)
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_user_repository import (
    FakeUserRepository,
)
from sightcall_transcript_to_tutorial.main import app
from sightcall_transcript_to_tutorial.presentation.api.dependencies import (
    get_transcript_repository,
    get_user_repository,
)

client = TestClient(app)

VALID_TRANSCRIPT_JSON = '{"timestamp": "2025-02-26T20:36:06Z", "duration_in_ticks": 12345, "phrases": [{"offset_milliseconds": 0, "duration_in_ticks": 1.0, "display": "Hello", "speaker": 1, "locale": "en-US", "confidence": 0.9}]}'
INVALID_TRANSCRIPT_JSON = '{"phrases": []}'
OVERSIZED_TRANSCRIPT_JSON = (
    '{"timestamp": "2025-02-26T20:36:06Z", "duration_in_ticks": 12345, "phrases": [{"offset_milliseconds": 0, "duration_in_ticks": 1.0, "display": "'
    + ("A" * 1_000_000)
    + '", "speaker": 1, "locale": "en-US", "confidence": 0.9}]}'
)

TEST_USER_ID = "test-user-1"
TEST_GITHUB_ID = 42
TEST_USER_NAME = "fakeuser"


def get_auth_cookies(user_id=TEST_USER_ID, github_id=TEST_GITHUB_ID, username=TEST_USER_NAME):
    """Create authentication cookies with JWT token for cookie-based auth"""
    payload = {"user_id": user_id, "github_id": github_id, "username": username}
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return {"access_token": token}


@pytest.fixture(autouse=True)
def setup_test_user():
    user_repo = FakeUserRepository()
    user_repo.save(User(user_id=UserId(TEST_USER_ID), name=TEST_USER_NAME, github_id=TEST_GITHUB_ID))
    app.dependency_overrides[get_user_repository] = lambda: user_repo


@pytest.fixture(autouse=True)
def override_transcript_repo():
    fake_repo = FakeTranscriptRepository()
    app.dependency_overrides[get_transcript_repository] = lambda: fake_repo
    yield
    app.dependency_overrides.pop(get_transcript_repository, None)


class TestTranscriptUploadAPI:
    def test_should_upload_transcript_successfully(self):
        response = client.post(
            "/transcripts",
            files={"file": ("transcript.json", io.BytesIO(VALID_TRANSCRIPT_JSON.encode()), "application/json")},
            cookies=get_auth_cookies(),
        )
        print(response.json())
        assert response.status_code == 201
        assert "id" in response.json()

    def test_should_reject_invalid_transcript_json(self):
        response = client.post(
            "/transcripts",
            files={"file": ("transcript.json", io.BytesIO(INVALID_TRANSCRIPT_JSON.encode()), "application/json")},
            cookies=get_auth_cookies(),
        )
        assert response.status_code == 422 or response.status_code == 400
        assert "error" in response.json() or "detail" in response.json()

    def test_should_reject_oversized_transcript(self):
        response = client.post(
            "/transcripts",
            files={"file": ("transcript.json", io.BytesIO(OVERSIZED_TRANSCRIPT_JSON.encode()), "application/json")},
            cookies=get_auth_cookies(),
        )
        assert response.status_code == 422 or response.status_code == 400
        assert "error" in response.json() or "detail" in response.json()

    def test_should_reject_unauthenticated_upload(self):
        response = client.post(
            "/transcripts",
            files={"file": ("transcript.json", io.BytesIO(VALID_TRANSCRIPT_JSON.encode()), "application/json")},
        )
        assert response.status_code == 401
        assert "error" in response.json() or "detail" in response.json()

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from sightcall_transcript_to_tutorial.domain.config.settings import settings
from sightcall_transcript_to_tutorial.domain.entities.transcript import Transcript
from sightcall_transcript_to_tutorial.domain.entities.user import User
from sightcall_transcript_to_tutorial.domain.value_objects.transcript_id import TranscriptId
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_transcript_repository import (
    FakeTranscriptRepository,
)
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_tutorial_repository import (
    FakeTutorialRepository,
)
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_user_repository import (
    FakeUserRepository,
)
from sightcall_transcript_to_tutorial.main import app
from sightcall_transcript_to_tutorial.presentation.api.dependencies import (
    get_transcript_repository,
    get_tutorial_repository,
    get_user_repository,
)

client = TestClient(app)

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


@pytest.mark.e2e
@pytest.mark.slow
def test_should_generate_tutorial_success():
    # Arrange: Insert a test transcript into the DB
    transcript_id = "test-transcript-1"
    transcript_content = "How to reset password in Gmail?"
    transcript = Transcript(TranscriptId(transcript_id), content=transcript_content)
    transcript_repository = FakeTranscriptRepository()
    tutorial_repository = FakeTutorialRepository()
    app.dependency_overrides[get_transcript_repository] = lambda: transcript_repository
    app.dependency_overrides[get_tutorial_repository] = lambda: tutorial_repository
    transcript_repository.save(transcript)

    response = client.post(
        "/tutorials/generate",
        json={"transcript_id": transcript_id},
        cookies=get_auth_cookies(),
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["title"], str) and data["title"].strip() != ""
    assert isinstance(data["content"], str) and data["content"].strip() != ""


@pytest.mark.e2e
def test_should_return_error_on_generation_failure():
    # Use a non-existent transcript_id
    response = client.post(
        "/tutorials/generate",
        json={"transcript_id": "non-existent-id"},
        cookies=get_auth_cookies(),
    )
    # Accept either 400 or 500 depending on how the backend handles it
    assert response.status_code in (400, 422, 500)
    detail = response.json().get("detail")
    assert detail is not None


def _create_tutorial(client, user_id, tutorial_id, title, content):
    # Helper to insert a tutorial into the fake repo
    repo = client.app.dependency_overrides[get_tutorial_repository]()
    from datetime import datetime, timezone

    from sightcall_transcript_to_tutorial.domain.entities.tutorial import Tutorial
    from sightcall_transcript_to_tutorial.domain.value_objects.tutorial_id import TutorialId
    from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId

    tutorial = Tutorial(
        tutorial_id=TutorialId(tutorial_id),
        title=title,
        content=content,
        user_id=UserId(user_id),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    repo.save(tutorial)
    return tutorial


def test_list_tutorials_should_return_only_owned_tutorials():
    # Arrange
    tutorial_repository = FakeTutorialRepository()
    app.dependency_overrides[get_tutorial_repository] = lambda: tutorial_repository
    _create_tutorial(client, TEST_USER_ID, "tut1", "Title 1", "Content 1")
    _create_tutorial(client, "other-user", "tut2", "Title 2", "Content 2")
    _create_tutorial(client, TEST_USER_ID, "tut3", "Title 3", "Content 3")
    # Act
    response = client.get("/tutorials", cookies=get_auth_cookies())
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    ids = [item["id"] for item in data["items"]]
    assert set(ids) == {"tut1", "tut3"}


def test_list_tutorials_should_support_pagination_and_search():
    tutorial_repository = FakeTutorialRepository()
    app.dependency_overrides[get_tutorial_repository] = lambda: tutorial_repository
    for i in range(5):
        _create_tutorial(client, TEST_USER_ID, f"tut{i}", f"Special {i}", f"Content {i}")
    # Page 2, page_size 2
    response = client.get("/tutorials?page=2&page_size=2", cookies=get_auth_cookies())
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert len(data["items"]) == 2
    # Search
    response = client.get("/tutorials?search=Special 3", cookies=get_auth_cookies())
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Special 3"


def test_get_tutorial_by_id_should_return_tutorial_if_owner():
    tutorial_repository = FakeTutorialRepository()
    app.dependency_overrides[get_tutorial_repository] = lambda: tutorial_repository
    _create_tutorial(client, TEST_USER_ID, "tut1", "Title 1", "Content 1")
    response = client.get("/tutorials/tut1", cookies=get_auth_cookies())
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "tut1"
    assert data["title"] == "Title 1"
    assert data["content"] == "Content 1"
    assert data["user_id"] == TEST_USER_ID


def test_get_tutorial_by_id_should_return_404_if_not_found_or_not_owner():
    tutorial_repository = FakeTutorialRepository()
    app.dependency_overrides[get_tutorial_repository] = lambda: tutorial_repository
    # Not found
    response = client.get("/tutorials/nonexistent", cookies=get_auth_cookies())
    assert response.status_code == 404
    # Not owner
    _create_tutorial(client, "other-user", "tut2", "Title 2", "Content 2")
    response = client.get("/tutorials/tut2", cookies=get_auth_cookies())
    assert response.status_code == 404


def test_patch_tutorial_should_update_title_and_content_if_owner():
    tutorial_repository = FakeTutorialRepository()
    app.dependency_overrides[get_tutorial_repository] = lambda: tutorial_repository
    _create_tutorial(client, TEST_USER_ID, "tut1", "Old Title", "Old Content")
    patch_data = {"title": "New Title", "content": "New Content"}
    response = client.patch("/tutorials/tut1", json=patch_data, cookies=get_auth_cookies())
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["content"] == "New Content"


def test_patch_tutorial_should_return_404_if_not_found_or_not_owner():
    tutorial_repository = FakeTutorialRepository()
    app.dependency_overrides[get_tutorial_repository] = lambda: tutorial_repository
    # Not found
    patch_data = {"title": "New Title"}
    response = client.patch("/tutorials/nonexistent", json=patch_data, cookies=get_auth_cookies())
    assert response.status_code == 404
    # Not owner
    _create_tutorial(client, "other-user", "tut2", "Title 2", "Content 2")
    response = client.patch("/tutorials/tut2", json=patch_data, cookies=get_auth_cookies())
    assert response.status_code == 404


def test_patch_tutorial_should_validate_input():
    tutorial_repository = FakeTutorialRepository()
    app.dependency_overrides[get_tutorial_repository] = lambda: tutorial_repository
    _create_tutorial(client, TEST_USER_ID, "tut1", "Old Title", "Old Content")
    # Empty title
    patch_data = {"title": ""}
    response = client.patch("/tutorials/tut1", json=patch_data, cookies=get_auth_cookies())
    assert response.status_code == 422 or response.status_code == 400
    # Empty content
    patch_data = {"content": ""}
    response = client.patch("/tutorials/tut1", json=patch_data, cookies=get_auth_cookies())
    assert response.status_code == 422 or response.status_code == 400

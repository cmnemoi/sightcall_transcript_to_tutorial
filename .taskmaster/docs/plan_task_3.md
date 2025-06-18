# Plan for Task 3: Create Transcript Upload API with Clean Architecture

**Task 3 Objective:**
Implement transcript upload functionality with proper layer separation and validation, following Clean Architecture principles.

---

## Codebase Analysis Summary

- No transcript upload API, router, or schema currently exists; these must be created from scratch.
- The `Transcript` domain entity and `TranscriptId` value object are implemented and tested.
- Transcript repository interfaces and both SQLAlchemy and in-memory fake implementations exist and are tested.
- **Transcripts will be stored directly in the database; no file storage gateway or external file storage is required.**
- No application command for uploading transcripts exists; this must be created.
- No TDD/unit/integration/e2e tests for upload exist; these must be added.
- Authentication and JWT middleware are present and can be reused for securing the upload endpoint.
- The project follows strict Clean Architecture, TDD, and domain-driven naming conventions.

---

## Implementation Plan

### 1. Add/Update Dependencies
- Ensure FastAPI and Pydantic are up to date for file upload support.
- Add any required libraries for file handling (if not already present).

### 2. Domain Layer
- **Entities:**
  - Review and, if needed, enhance the `Transcript` entity to support validation for uploaded content (e.g., JSON schema, file size, required fields).
- **Value Objects:**
  - Ensure `TranscriptId` and any other relevant value objects are sufficient for upload validation.
- **Exceptions:**
  - Define domain-specific exceptions for invalid transcript uploads in `domain/exceptions/` (e.g., `InvalidTranscriptError`).

### 3. Application Layer
- **Commands:**
  - Implement `UploadTranscriptCommand` in `application/commands/` to encapsulate the upload logic.
  - Command should validate input, create a `Transcript` entity, and persist it via the repository.
- **Command Handler:**
  - Implement `UploadTranscriptCommandHandler` to coordinate validation, entity creation, and repository interaction.

### 4. Infrastructure Layer
- **Repositories:**
  - Ensure `SQLAlchemyTranscriptRepository` supports saving new transcripts from uploads.
  - Ensure `FakeTranscriptRepository` supports upload scenarios for unit tests.

### 5. Presentation Layer
- **Routers:**
  - Create `transcripts.py` router in `presentation/api/routers/`.
  - Implement `POST /transcripts` endpoint accepting multipart form data (file upload).
  - Secure the endpoint with authentication middleware.
- **Schemas:**
  - Create `transcript.py` in `presentation/api/schemas/` for request/response models using Pydantic.
  - Define schemas for upload requests (file) and responses (success, error).
  - Parse the uploaded file, validate its JSON structure, and pass the content to the application layer for persistence.

### 6. Testing
- **Unit Tests:**
  - Write TDD-style tests for the `Transcript` entity (validation), `UploadTranscriptCommand`, and command handler in `tests/unit/`.
  - Use `FakeTranscriptRepository` for isolation.
- **Integration Tests:**
  - Add tests for `SQLAlchemyTranscriptRepository` in `tests/integration/` to verify DB persistence of uploaded transcripts.
- **E2E Tests:**
  - Add end-to-end tests in `tests/e2e/` for the upload API, covering authentication, file validation, and DB persistence.
  - Test both valid and invalid upload scenarios (e.g., missing fields, invalid JSON, oversized files).

### 7. Documentation
- Document the new API endpoint and request/response formats in `README.md` or API docs.
- Add usage examples for frontend integration.

---

## Notes
- **Clean Architecture:** Strictly separate domain, application, infrastructure, and presentation concerns. All business logic and validation must reside in the domain/application layers.
- **TDD:** Write failing tests before implementing production code. Use in-memory fakes for all service/repository unit tests.
- **Validation:** Ensure robust validation for uploaded transcripts (file type, schema, size, required fields).
- **Security:** Require authentication for upload. Validate and sanitize all inputs to prevent injection or file-based attacks.
- **Ubiquitous Language:** Use clear, domain-driven names for all new classes, functions, and endpoints. 
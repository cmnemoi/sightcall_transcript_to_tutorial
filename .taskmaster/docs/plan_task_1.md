# Plan for Task 1: Setup Database Schema with Clean Architecture

**Task 1 Objective:**
Create PostgreSQL database schema with domain entities, repository interfaces, and infrastructure implementations, following Clean Architecture.

---

## Codebase Analysis Summary

- No domain entities, value objects, repository interfaces, or exceptions are currently implemented (all relevant directories are empty).
- No infrastructure repository implementations or test fakes exist (all relevant directories are empty).
- No SQLAlchemy, Alembic, or database-related dependencies are present in `pyproject.toml`.
- No database or migration logic is present in the codebase.
- Docker Compose is set up with a PostgreSQL service (`compose.yml`), exposing the database to the backend, but the backend does not yet connect to it.
- No environment variable or config logic for database connection is present.
- No tests exist for domain entities, repositories, or database logic; only a root FastAPI endpoint test is present.

---

## Implementation Plan

### 1. Add Required Dependencies
- Add `SQLAlchemy`, `alembic`, and both sync (`psycopg2`) and async (`asyncpg`, `SQLAlchemy[asyncio]`) PostgreSQL drivers to backend dependencies in `pyproject.toml`.
- Add `testcontainers[postgres]` for integration testing in the test dependency group.

### 2. Domain Layer
- **Entities:**
  - Implement `User`, `Transcript`, and `Tutorial` as Python classes in `domain/entities/`.
  - Use value objects for IDs and other complex fields.
- **Value Objects:**
  - Implement value objects (e.g., `UserId`, `TranscriptId`, `TutorialId`, etc.) in `domain/value_objects/`.
- **Exceptions:**
  - Define domain-specific exceptions in `domain/exceptions/`.
- **Repository Interfaces:**
  - Define abstract repository interfaces (`UserRepositoryInterface`, `TranscriptRepositoryInterface`, `TutorialRepositoryInterface`) in `domain/repositories/`.
- **Domain Models:**
  - Define `User`, `Transcript`, and `Tutorial` as SQLAlchemy models directly in a new `domain/models/` directory. These models will serve as both the domain objects and the persistence models.

### 3. Application Layer
- No immediate changes, but ensure commands/queries can depend on repository interfaces.

### 4. Infrastructure Layer
- **SQLAlchemy Models:**
  - Implement SQLAlchemy models in `infrastructure/for_production/repositories/` mapping to domain entities.
- **Repository Implementations:**
  - Implement concrete repository classes for each entity, adhering to the interfaces.
- **Database Migrations:**
  - Initialize Alembic in the backend.
  - Create an initial migration based on the models defined in `domain/models/`.

### 5. Configuration
- Implement a config module in `domain/config/` to load DB connection info from environment variables.

### 6. Testing
- **Unit Tests:**
  - Write TDD-style tests for the domain models and value objects in `tests/unit/`.
- **Fake Repositories:**
  - Implement in-memory fake repositories in `infrastructure/for_tests/repositories/` for use in unit tests.
- **Integration Tests:**
  - Use `testcontainers[postgres]` to spin up a PostgreSQL container and test real repository implementations in `tests/integration/`.

### 7. Docker Compose
- Ensure backend and db services are correctly networked.
- Document `.env` setup for DB connection.

---

## Notes
- **Architectural Choice**: We are intentionally using a single model for both domain and persistence to simplify the architecture. This is a pragmatic trade-off that slightly diverges from a strict interpretation of Clean Architecture but accelerates development.
- Use TDD: write failing tests before implementing production code.
- Use in-memory fakes for unit tests, not mocks or in-memory DBs.
- Use domain-driven vocabulary and clear, intention-revealing names. 
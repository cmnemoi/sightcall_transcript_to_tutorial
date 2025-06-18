# Plan for Task 6: Implement Tutorial CRUD with Clean Architecture

## 1. Domain Layer
- **Enhance `Tutorial` Entity**:
  - Add user ownership (`user_id: UserId`) to the `Tutorial` entity.
  - Add `created_at` and `updated_at` fields for filtering/sorting.
  - Add update methods and validation for title/content.
- **Update Value Objects**:
  - Ensure `UserId` is used for ownership.
- **Update Repository Interface**:
  - Add methods for:
    - Listing tutorials (with filtering, pagination, search).
    - Updating tutorials (partial update for PATCH).
    - Ownership validation.

## 2. Application Layer
- **Queries**:
  - `GetTutorialsQuery`: List tutorials for a user, with filtering (date, title search), pagination.
  - `GetTutorialByIdQuery`: Fetch a single tutorial by ID, with ownership check.
- **Commands**:
  - `UpdateTutorialCommand`: Update a tutorial's title/content, with ownership and validation.
- **Handlers**:
  - Implement handlers for the above, using repository and value objects.

## 3. Infrastructure Layer
- **SQLAlchemy Model**:
  - Add `user_id`, `created_at`, `updated_at` columns to `SQLAlchemyTutorial`.
  - Update `from_domain`/`to_domain` methods.
  - Update Alembic migration for schema changes.
- **Repository Implementation**:
  - Implement new repository methods for list, update, filtering, and ownership in in infrastructure/for_tests/ and infrastructure/for_production/
  - Support pagination and search in SQL queries

## 4. Presentation Layer (API)
- **Schemas**:
  - Add Pydantic models for:
    - Tutorial list response (with pagination thanks to FastAPI).
    - Tutorial detail.
    - Tutorial update request (PATCH).
- **Routers**:
  - Add endpoints:
    - `GET /tutorials`: List tutorials (with filters, pagination).
    - `GET /tutorials/{tutorial_id}`: Get tutorial by ID.
    - `PATCH /tutorials/{tutorial_id}`: Update tutorial (title/content).
  - Add user ownership validation (use current user from dependency).
  - Support filtering by creation date and search by title.

## 5. Testing
- **Unit Tests**:
  - For new/updated domain logic (entity, value objects).
  - For application commands/queries (using fakes).
- **Integration Tests**:
  - For repository (SQLAlchemy) with new methods.
- **E2E/API Tests**:
  - For all new endpoints, including:
    - Ownership enforcement.
    - Filtering, pagination, and search.
    - Update and validation errors.

## 6. Migration & Refactoring
- **Data Migration**:
  - Write Alembic migration for new columns.
- **Refactor**:
  - Update all usages of `Tutorial` to include new fields.
  - Ensure all layers are decoupled and follow Clean Architecture.

## File Placement
- **Domain**: `domain/entities/tutorial.py`, `domain/value_objects/user_id.py`, `domain/repositories/tutorial_repository_interface.py`
- **Application**: `application/queries/get_tutorials_query.py`, `application/queries/get_tutorial_by_id_query.py`, `application/commands/update_tutorial_command.py`
- **Infrastructure**: `infrastructure/for_production/models/sqlalchemy_tutorial.py`, `infrastructure/for_production/repositories/sqlalchemy_tutorial_repository.py`, Alembic migration
- **Presentation**: `presentation/api/routers/tutorial.py`, `presentation/api/schemas/tutorial.py`
- **Tests**: `tests/unit/domain/entities/test_tutorial.py`, `tests/unit/application/queries/`, `tests/unit/application/commands/`, `tests/integration/repositories/`, `tests/e2e/test_tutorial_api.py`

## Next Steps
1. Write failing unit tests for new/updated domain logic and application handlers (TDD).
2. Implement domain/entity changes and repository interface.
3. Implement application queries/commands and handlers.
4. Update infrastructure models, repositories, and migrations.
5. Add/extend API endpoints and schemas.
6. Write/extend integration and e2e tests.
7. Refactor and ensure all tests pass. 
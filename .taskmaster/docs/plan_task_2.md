# Plan for Task 2: Implement GitHub OAuth 2.0 Authentication with Clean Architecture

**Task 2 Objective:**
Create authentication system with domain services, application commands/queries, and infrastructure integration, following Clean Architecture principles.

---

## Implementation Plan

### 1. Add Required Dependencies
- Add `python-jose` for JWT creation/validation.
- Add `httpx` for GitHub API calls.
- Add `authlib` for OAuth 2.0 flow.

### 2. Domain Layer
- **Entities:**
  - Define `AuthenticatedUser` entity in `domain/entities/` to represent authenticated users (GitHub ID, username, email).
- **Service Interfaces:**
  - Define `AuthenticationGatewayInterface` in `domain/gateways/` for authentication contract (login, callback, JWT handling).

### 3. Application Layer
- **Commands/Queries:**
  - Implement `LoginCommand` in `application/commands/` to initiate OAuth flow.
  - Implement `GetAuthenticatedUserQuery` in `application/queries/` to handle callback and user authentication.

### 4. Infrastructure Layer
- **Gateways:**
  - Implement `GitHubAuthenticationGateway` in `infrastructure/for_production/gateways/` for OAuth and JWT logic.
  - Use `python-jose` for JWT creation/validation.
  - Store/retrieve user data via `UserRepository`.
- **Fakes for Testing:**
  - Implement `FakeAuthenticationGateway` in `infrastructure/for_tests/gateways/` for unit tests.

### 5. Presentation Layer
- **Routers:**
  - Create `auth` router in `presentation/api/routers/` with endpoints:
    - `GET /auth/github/login` (redirect to GitHub)
    - `GET /auth/github/callback` (handle OAuth callback)
- **Schemas:**
  - Define request/response schemas in `presentation/api/schemas/` for authentication endpoints.
- **JWT Middleware:**
  - Implement JWT middleware in `presentation/api/middlewares` for protected routes.

### 6. Testing
- **Unit Tests:**
  - Write TDD-style tests for domain authentication logic and service interface in `tests/unit/`.
  - Test JWT creation/validation in isolation.
  - Use `FakeAuthenticationGateway` and `FakeUserRepository` for application layer unit tests.
- **Integration Tests:**
  - Test `GitHubAuthenticationGateway` in `tests/integration/` with real GitHub API calls.
- **E2E Tests:**
  - Add end-to-end tests for login and callback flow in `tests/e2e/` with real GitHub API calls and real database (happy path only).

### 7. Configuration
- Add GitHub OAuth client ID/secret and JWT secret to environment variables/config (`domain/config/settings.py`).
- Document required environment variables in `README.md`.

---

## Notes
- **Clean Architecture:** Strictly separate domain, application, infrastructure, and presentation concerns.
- **TDD:** Write failing tests before implementing production code.
- **Fakes over Mocks:** Use in-memory fakes for all service/repository unit tests.
- **Security:** Never log secrets; handle tokens securely.
- **Ubiquitous Language:** Use clear, domain-driven names for all new classes and functions. 
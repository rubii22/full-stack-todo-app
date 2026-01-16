# Implementation Plan: Todo Backend API

**Branch**: `1-backend-api` | **Date**: 2026-01-15 | **Spec**: [specs/1-backend-api/spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-backend-api/spec.md`

## Summary

Develop a secure, production-ready RESTful API for the Todo Full-Stack Web Application using Python FastAPI, SQLModel ORM, and Neon Serverless PostgreSQL. The API will implement complete CRUD operations for tasks with JWT-based authentication and authorization using Better Auth integration, ensuring strict user data isolation and comprehensive security measures.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel ORM, Pydantic, PyJWT, Neon PostgreSQL driver
**Storage**: Neon Serverless PostgreSQL with proper indexing and foreign key constraints
**Testing**: pytest with test containers for database integration tests
**Target Platform**: Linux server deployment with Docker containerization
**Project Type**: Web backend API service
**Performance Goals**: 95th percentile response time under 500ms, 99.9% authentication validation under 100ms
**Constraints**: 100% user data isolation, 99.5% uptime during peak usage, 99% successful CRUD operations
**Scale/Scope**: Support 1000+ concurrent users with proper rate limiting and connection pooling

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the project constitution, the following gates must be satisfied:
- Security: JWT-based authentication with proper token validation and user isolation
- Performance: Response times within specified limits
- Scalability: Support for concurrent users with proper database connection handling
- Maintainability: Clean separation of concerns with proper API design

## Project Structure

### Documentation (this feature)

```text
specs/1-backend-api/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── todo-api.yaml    # OpenAPI specification
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py          # FastAPI application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py      # User model (managed by Better Auth)
│   │   └── task.py      # Task model with SQLModel ORM
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py      # Pydantic schemas for user data
│   │   └── task.py      # Pydantic schemas for task operations
│   ├── database/
│   │   ├── __init__.py
│   │   ├── config.py    # Database configuration and connection
│   │   └── session.py   # Database session management
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── middleware.py # JWT authentication middleware
│   │   └── utils.py     # JWT token utilities
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py      # Dependency injection utilities
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py # Main API router
│   │       └── tasks.py # Task CRUD endpoints
│   └── core/
│       ├── __init__.py
│       ├── config.py    # Application configuration
│       └── security.py  # Security utilities
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # Test configuration
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_auth.py # Authentication unit tests
│   │   └── test_models.py # Model unit tests
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_tasks.py # Task API integration tests
│   │   └── test_auth.py # Authentication integration tests
│   └── fixtures/
│       ├── __init__.py
│       └── database.py  # Test database fixtures
├── requirements.txt     # Python dependencies
├── requirements-dev.txt # Development dependencies
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
└── Dockerfile           # Containerization
```

**Structure Decision**: Web application backend service following FastAPI best practices with clean architecture, separating models, schemas, API routes, database configuration, and authentication logic into distinct modules.

## Backend Architecture Sketch

### Layer Architecture

```
┌─────────────────────────────────────────┐
│            API Routes Layer             │
│  (FastAPI endpoints in api/v1/tasks.py) │
├─────────────────────────────────────────┤
│         Dependencies/Middleware         │
│  (JWT auth, current_user dependency)    │
├─────────────────────────────────────────┤
│             ORM/Models Layer            │
│    (SQLModel classes in models/task.py) │
├─────────────────────────────────────────┤
│          DB Connection Layer            │
│ (engine, session in database/config.py) │
└─────────────────────────────────────────┘
```

### Detailed Component Interactions

1. **API Routes Layer** (`api/v1/tasks.py`)
   - FastAPI endpoints handling HTTP requests
   - Uses dependency injection for authentication
   - Maps Pydantic schemas to/from database models
   - Handles query parameters (status, sort, pagination)

2. **Dependencies/Middleware Layer** (`auth/`, `api/deps.py`)
   - JWT token extraction and validation
   - User identity extraction from token
   - Global authentication enforcement
   - Error handling and response formatting

3. **ORM/Models Layer** (`models/`)
   - SQLModel database models with relationships
   - Pydantic validation schemas
   - Database query methods
   - Index definitions for performance

4. **DB Connection Layer** (`database/`)
   - Connection pooling and session management
   - Async/await support for concurrent requests
   - Transaction handling and cleanup
   - Connection via DATABASE_URL to Neon PostgreSQL

## Incremental Implementation Approach

### Phase 1: Database Foundation
1. Implement database connection (`database/config.py`, `database/session.py`)
2. Define SQLModel models (`models/task.py`) with proper relationships and indexes
3. Create database tables and test connection
4. Implement basic CRUD operations at model level

### Phase 2: Authentication Infrastructure
1. Implement JWT utilities (`auth/utils.py`) for token verification
2. Create authentication dependency (`api/deps.py`) to extract current_user
3. Implement global authentication middleware for all `/api/` routes
4. Test JWT validation with valid/invalid/expired tokens

### Phase 3: Core API Endpoints
1. Implement Task CRUD routes (`api/v1/tasks.py`) with proper user isolation
2. Add query parameter support (status filtering, sorting, pagination)
3. Implement proper error handling with HTTPException
4. Test individual endpoints with valid/invalid authentication

### Phase 4: Integration & Testing
1. End-to-end testing with multiple users and data isolation
2. Performance testing with concurrent requests
3. Security validation (cross-user access prevention)
4. Frontend integration testing

## Key Technology Decisions & Trade-offs

### JWT Verification Library
- **Choice**: PyJWT (recommended for compatibility with Better Auth HS256)
- **Alternative**: fastapi-jwt-auth, built-in FastAPI OAuth2PasswordBearer
- **Trade-offs**:
  - PyJWT is lightweight and direct for shared secret decoding
  - Others may add overhead or require extra configuration
  - PyJWT provides fine-grained control over token validation

### Authentication Enforcement Method
- **Choice**: Global middleware for all `/api/` routes
- **Alternative**: Per-route dependencies
- **Trade-offs**:
  - Middleware ensures consistent application and easier maintenance
  - Dependencies allow more granular control but require repetitive application
  - Global approach reduces code duplication and potential for oversight

### User Extraction Method
- **Choice**: Decode token in dependency to get user_id only
- **Alternative**: Store full user object after DB lookup
- **Trade-offs**:
  - user_id only is sufficient and maintains stateless design
  - Full user object adds DB lookup but enables richer features
  - Statelessness aligns with JWT principles and Better Auth integration

### Error Handling Strategy
- **Choice**: Centralized HTTPException raising with custom exception handlers
- **Alternative**: Scattered error handling throughout code
- **Trade-offs**:
  - Centralized approach is simpler for consistent 401/403 responses
  - Custom handlers allow better logging and standardized formatting
  - Consistent error responses improve frontend integration

## Testing Strategy

### Unit Tests
- JWT decode/verify function (valid, invalid signature, expired, missing claims)
- Model validation and database operations
- Utility functions in auth/utils.py

### Integration Tests
- Using TestClient to test each endpoint
- Valid token with correct user data access
- Invalid/missing/expired token handling (401 responses)
- Cross-user data isolation (user A cannot access user B's tasks)
- Query parameter functionality (status, sort, pagination)

### Database Tests
- Persistence validation (tasks created/updated/deleted only for owner)
- Indexing performance verification
- Connection handling via DATABASE_URL
- Concurrent access and transaction management

### Security Validation
- Token leak prevention
- Stateless design validation
- No shared session vulnerabilities
- User data isolation enforcement

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple layered architecture | Security and maintainability | Direct API to database would violate user isolation requirements |
| JWT middleware | Stateless authentication with Better Auth integration | Session-based auth would conflict with Better Auth's token system |
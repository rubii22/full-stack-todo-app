# Feature Specification: Todo Backend API

**Feature Branch**: `1-backend-api`
**Created**: 2026-01-15
**Status**: Draft
**Input**: User description: "Backend for Phase II - Todo Full-Stack Web Application
Target audience: Multi-user system for task management, with secure API serving frontend requests in a production-ready environment
Focus: RESTful API implementation for task CRUD operations, user authentication verification via JWT tokens issued by Better Auth, and persistent data storage with strict user isolation in Neon Serverless PostgreSQL
Success criteria:

Implements all specified API endpoints exactly as defined in /specs/api/rest-endpoints.md (e.g., GET /api/tasks, POST /api/tasks, GET/PUT/DELETE/PATCH /api/tasks/{id}, with query params like status, sort), including user-specific filtering and ownership enforcement (tasks.user_id must match authenticated user)
Authentication integration: Uses middleware/dependency to verify JWT tokens from Better Auth (Authorization: Bearer <token>), extracts user ID/email from decoded token using shared BETTER_AUTH_SECRET, and restricts all operations to the authenticated user's data only (raise 401 if invalid/missing/expired token)
Database interactions: Uses SQLModel ORM to define and manage schema (users table managed by Better Auth, tasks table with fields: id, user_id (FK to users.id), title, description, completed, created_at, updated_at), proper indexing (on user_id, completed), connects via DATABASE_URL environment variable, and performs error-free CRUD operations with proper timestamps
Security enforced: Implements JWT validation middleware (using PyJWT or compatible library for verification with HS256 algorithm and shared secret), handles token expiry, returns 401 Unauthorized on invalid/missing tokens, stateless auth (no sessions), prevents data leaks between users, and eliminates vulnerabilities like shared DB sessions
Seamless frontend integration: Returns JSON responses using Pydantic models, handles errors gracefully with HTTPException, supports required query parameters (e.g., status: "all"/"pending"/"completed", sort: "created"/"title"/"due_date"), and ensures immediate compatibility with existing Next.js frontend API calls
Passes rigorous testing: No cross-user data access possible, all CRUD operations persist correctly and retrieve only owned tasks in Neon PostgreSQL, zero errors/warnings in API responses when called from frontend, follows backend CLAUDE.md conventions strictly (e.g., routes/ folder, models.py, db.py), and validates user isolation with multiple test users
Constraints:

Tech stack: Python FastAPI (latest), SQLModel ORM, Neon Serverless PostgreSQL; monorepo structure under /backend/ following CLAUDE.md guidelines (main.py as entry point, models.py for SQLModel classes, routes/ for endpoint handlers, db.py for connection/session management)
Reference specs: Strictly adhere to /specs/features/task-crud.md (user stories & acceptance criteria), /specs/features/authentication.md, /specs/api/rest-endpoints.md (full endpoint details), /specs/database/schema.md (exact table schema and indexes)
Development workflow: Update relevant specs first if needed, then implement incrementally via Claude Code references (e.g., "@specs/api/rest-endpoints.md implement GET /api/tasks with JWT auth", "@specs/database/schema.md create tasks model")
Environment: Integrate seamlessly with frontend via REST API calls; use docker-compose.yml for local development (cd backend && uvicorn main:app --reload --port 8000); shared environment variable BETTER_AUTH_SECRET for JWT signing/verification (same as frontend); DATABASE_URL for Neon connection
Design: Fully stateless authentication, all routes prefixed under /api/, user_id in URL paths for explicit ownership (even if redundant with token), no direct database access from frontend (API-only layer), use Pydantic for request/response validation
Timeline: Complete within Phase II to enable immediate full-stack testing; ensure backend is ready for Phase III (chatbot) extension
Not building:

Frontend implementation or components (already handled in /frontend/)
Custom authentication system or alternative libraries (strictly use Better Auth JWT integration only, no built-in FastAPI OAuth2PasswordBearer unless compatible)
Advanced features like real-time updates, chatbot integration (Phase III), or role-based access
Non-RESTful endpoints, custom token generation (Better Auth issues tokens), or alternative auth methods
Manual database migrations/schema changes outside SQLModel definitions (follow /specs/database/schema.md strictly; assume Better Auth handles users table)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Task Management (Priority: P1)

A registered user accesses the todo application and performs CRUD operations on their tasks. The user can create, read, update, and delete tasks via API calls, with all operations properly authenticated and restricted to their own data only through JWT token validation and user ID matching.

**Why this priority**: This is the core functionality of the todo application - users need to be able to manage their tasks securely with proper data isolation between users.

**Independent Test**: A user can authenticate with a valid Better Auth JWT token and perform all CRUD operations on their tasks via API endpoints, with the system properly enforcing that they can only access their own tasks and receive appropriate error responses when attempting to access others' data.

**Acceptance Scenarios**:

1. **Given** an authenticated user with valid JWT token, **When** they create a new task via POST /api/tasks, **Then** the task is saved with their user ID linked from the token and they receive a 201 Created response
2. **Given** an authenticated user requesting their tasks via GET /api/tasks, **When** they make the API call with valid credentials, **Then** they receive only their own tasks filtered by user_id and not tasks belonging to other users
3. **Given** an authenticated user attempting to access another user's task via GET /api/tasks/{id}, **When** they make the API call with valid token but different user's task ID, **Then** the system returns a 404 Not Found or 403 Forbidden response

---

### User Story 2 - JWT-Based Authentication and Authorization (Priority: P1)

A user with a valid JWT token issued by Better Auth can access protected API endpoints. The system verifies the JWT token using the shared BETTER_AUTH_SECRET, extracts the user ID from the decoded payload, and enforces that all operations are limited to the authenticated user's data only.

**Why this priority**: Without proper authentication and authorization, the system cannot ensure data isolation or prevent unauthorized access to user data, which is critical for a multi-user system.

**Independent Test**: When a user makes an API request with a valid JWT token, the system successfully authenticates them and allows access to their own data; when an invalid, missing, or expired token is provided, the system returns a 401 Unauthorized response.

**Acceptance Scenarios**:

1. **Given** a request with a valid JWT token from Better Auth, **When** the API validates the token using HS256 algorithm and shared secret, **Then** the user ID is extracted and operations are scoped to that user's data
2. **Given** a request with an invalid, missing, or expired JWT token, **When** the API processes the request, **Then** a 401 Unauthorized response is returned
3. **Given** a request with a malformed JWT token, **When** the API attempts to decode it, **Then** a 401 Unauthorized response is returned with appropriate error message

---

### User Story 3 - Task Query and Filtering with User Isolation (Priority: P2)

Authenticated users can retrieve their tasks with various filtering and sorting options while maintaining strict user data isolation. The API supports query parameters for filtering tasks by status (all/pending/completed) and sorting options, all while ensuring users can only access their own data.

**Why this priority**: This enhances the user experience by allowing them to efficiently find and organize their tasks based on their preferences while maintaining security.

**Independent Test**: A user can request their tasks with query parameters (e.g., status=completed, sort=created_at) and receive a filtered and sorted list of their own tasks without any data from other users appearing in the results.

**Acceptance Scenarios**:

1. **Given** an authenticated user requesting tasks with status filter, **When** they call GET /api/tasks?status=completed, **Then** they receive only their completed tasks with user_id matching their authenticated ID
2. **Given** an authenticated user requesting sorted tasks, **When** they call GET /api/tasks?sort=created_at&order=desc, **Then** they receive their tasks sorted by creation date in descending order, with user_id matching their authenticated ID
3. **Given** an authenticated user requesting paginated results, **When** they call GET /api/tasks?page=1&limit=10, **Then** they receive their first 10 tasks with user_id matching their authenticated ID

---

### Edge Cases

- What happens when a user attempts to access a task that belongs to a different user?
- How does the system handle expired JWT tokens during API requests?
- What occurs when the database connection fails during a transaction?
- How does the system handle malformed JWT tokens?
- What happens when a user tries to update or delete a task that no longer exists or belongs to another user?
- How does the system handle concurrent requests from the same user?
- What occurs when the database is under high load or experiencing performance issues?
- How does the system handle invalid query parameters or SQL injection attempts?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide RESTful API endpoints for task CRUD operations (GET/POST/PUT/DELETE) following standard HTTP methods and status codes, located under /api/ prefix
- **FR-002**: System MUST verify JWT tokens from Better Auth using HS256 algorithm with shared BETTER_AUTH_SECRET and extract user ID for all protected endpoints
- **FR-003**: System MUST ensure users can only access, modify, and delete their own tasks by matching user_id in database records to authenticated user ID
- **FR-004**: System MUST return appropriate HTTP status codes (200, 201, 401, 403, 404, 422, 500) based on request outcomes and security validation
- **FR-005**: System MUST handle query parameters for task filtering (status: all/pending/completed, search terms) and sorting (field, direction) while maintaining user isolation
- **FR-006**: System MUST store all data persistently in Neon Serverless PostgreSQL database using SQLModel ORM with proper indexing and foreign key relationships
- **FR-007**: System MUST validate input data using Pydantic models and return appropriate error messages for validation failures
- **FR-008**: System MUST implement proper error handling with HTTPException for various failure scenarios including database errors and authentication failures
- **FR-009**: System MUST support pagination for task listings to handle large datasets efficiently (page, limit parameters)
- **FR-010**: System MUST enforce data integrity constraints at the database level and maintain proper timestamps (created_at, updated_at)
- **FR-011**: System MUST use stateless authentication with no server-side session storage, relying solely on JWT token validation
- **FR-012**: System MUST implement rate limiting to prevent abuse and ensure fair usage across all users
- **FR-013**: System MUST validate that user_id in URL paths matches the authenticated user's ID for explicit ownership verification
- **FR-014**: System MUST return JSON responses using Pydantic models for consistent data formatting

### Key Entities

- **User**: Represents a registered user managed by Better Auth with unique identifier, authentication tokens, and associated tasks (user_id foreign key relationship)
- **Task**: Represents a user's task with properties: id (primary key), user_id (foreign key to users.id), title (required), description (optional), completed (boolean, default: false), created_at (timestamp), updated_at (timestamp), with proper indexing on user_id and completed fields

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All API endpoints return responses within 500ms under normal load conditions with 95th percentile response time under 2 seconds
- **SC-002**: Authentication verification completes in under 100ms with 99.9% success rate using JWT validation with shared secret
- **SC-003**: Users can only access their own tasks with 100% data isolation enforcement - no cross-user data access is possible
- **SC-004**: API achieves 99.5% uptime during peak usage hours with graceful degradation during maintenance
- **SC-005**: Task CRUD operations complete successfully 99% of the time with proper error handling for edge cases
- **SC-006**: No data leaks occur between different users' task data during concurrent usage scenarios
- **SC-007**: Frontend can successfully integrate with all API endpoints without errors, using standard HTTP methods and JSON responses
- **SC-008**: System handles 1000+ concurrent users without performance degradation and maintains user data isolation
- **SC-009**: API endpoint implementations exactly match specifications in /specs/api/rest-endpoints.md with full feature parity
- **SC-010**: Database operations complete efficiently with proper indexing and foreign key constraints preventing data corruption
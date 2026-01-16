# ADR: Backend API Architecture for Todo Application

## Status
Accepted

## Date
2026-01-15

## Context
For the Todo Full-Stack Web Application, we need to establish a robust, secure, and scalable backend API that integrates with Better Auth for JWT-based authentication, supports user data isolation, and provides reliable task management functionality.

## Decision

We have selected the following architectural approach:

### Technology Stack
- **Framework**: FastAPI for its modern Python capabilities, automatic API documentation, and excellent performance with async operations
- **ORM**: SQLModel for its combination of SQLAlchemy's power with Pydantic's validation, developed by the same author as FastAPI
- **Database**: Neon Serverless PostgreSQL for its automatic scaling, instant branching, and serverless capabilities
- **Authentication**: JWT token validation with Better Auth integration using shared BETTER_AUTH_SECRET

### Security Architecture
- **Authentication**: Stateless JWT token validation middleware that extracts user ID from Better Auth tokens
- **Authorization**: User data isolation enforced at both API and database levels with user_id foreign key constraints
- **Access Control**: All endpoints require valid JWT tokens with proper user ID matching

### API Design
- **Pattern**: RESTful endpoints with proper HTTP methods and status codes
- **Endpoints**: CRUD operations on /api/tasks with support for filtering, sorting, and pagination
- **Error Handling**: HTTPException with appropriate status codes (200/201 for success, 401/403/404 for access control, 422 for validation)

## Alternatives Considered

### Framework Alternatives
- Flask: More mature but slower performance and less built-in validation
- Django: Overkill for API-only application with unnecessary overhead
- Starlette: Too low-level requiring more boilerplate code

### ORM Alternatives
- SQLAlchemy Core: More verbose and doesn't integrate as seamlessly with FastAPI/Pydantic
- Tortoise ORM: Async-only which may complicate certain operations
- Peewee: Less modern and fewer features than SQLModel

### Database Alternatives
- Standard PostgreSQL: Requires more server management overhead
- MySQL: Less suitable for ORM mapping and modern features
- MongoDB: Not ideal for relational data with user-task relationships

### Authentication Alternatives
- Session-based: Would conflict with Better Auth's token system and require server-side state
- OAuth2 Password Flow: Different approach than Better Auth's token issuance system

## Consequences

### Positive
- FastAPI provides automatic API documentation and excellent developer experience
- SQLModel offers seamless integration between database models and API schemas
- Neon PostgreSQL provides automatic scaling without infrastructure management
- JWT tokens integrate cleanly with Better Auth's authentication system
- User isolation at both API and database levels provides defense in depth
- Modern async Python stack enables high performance and concurrency

### Negative
- Learning curve for team members unfamiliar with FastAPI/SQLModel
- Vendor lock-in to Neon PostgreSQL serverless platform
- Stateless authentication requires careful token management
- Additional complexity compared to simpler frameworks

## Implementation Notes

- Environment variables for sensitive data (DATABASE_URL, BETTER_AUTH_SECRET)
- Proper connection pooling for database operations
- Rate limiting to prevent abuse
- Comprehensive error handling with appropriate HTTP status codes
- Input validation using Pydantic models
- Proper indexing strategy for performance
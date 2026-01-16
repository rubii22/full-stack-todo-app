# Todo Backend API

This is the backend API for the Todo Full-Stack Web Application, built with FastAPI, SQLModel, and Neon Serverless PostgreSQL. It provides secure task management functionality with JWT-based authentication integrated with Better Auth.

## Features

- **Secure Task Management**: Full CRUD operations for user tasks
- **JWT Authentication**: Integration with Better Auth for secure authentication
- **User Data Isolation**: Strict enforcement that users can only access their own tasks
- **Query & Filtering**: Support for filtering, sorting, and pagination
- **Production Ready**: Rate limiting, comprehensive logging, and health checks

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel (combines SQLAlchemy + Pydantic)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT tokens from Better Auth
- **Validation**: Pydantic models

## API Endpoints

### Authentication

All API endpoints require a valid JWT token from Better Auth in the Authorization header:

```
Authorization: Bearer <jwt_token_here>
```

### Task Management

#### Get all tasks
```
GET /api/tasks?[status=all|pending|completed]&[sort=created_at|title|updated_at]&[order=asc|desc]&[page=1]&[limit=10]
```

#### Create a task
```
POST /api/tasks
Content-Type: application/json

{
  "title": "Sample Task",
  "description": "Task description (optional)",
  "completed": false
}
```

#### Get a specific task
```
GET /api/tasks/{task_id}
```

#### Update a task
```
PUT /api/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated Task Title",
  "description": "Updated description",
  "completed": true
}
```

#### Delete a task
```
DELETE /api/tasks/{task_id}
```

#### Health check
```
GET /health
```

## Environment Variables

Create a `.env` file in the backend root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your_better_auth_secret_key
JWT_ALGORITHM=HS256
ENVIRONMENT=development
DEBUG=false
```

## Running the Application

### Development

```bash
# Install dependencies with uv
uv sync

# Run the application
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

### Production

```bash
# Using gunicorn
uv run gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker

```bash
# Build the image
docker build -t todo-backend .

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e BETTER_AUTH_SECRET=... \
  -e ENVIRONMENT=production \
  todo-backend
```

## Testing

Run the tests using pytest with uv:

```bash
# Run all tests
uv run pytest

# Run unit tests
uv run pytest tests/unit/

# Run integration tests
uv run pytest tests/integration/
```

## Security

- JWT tokens are validated using the shared BETTER_AUTH_SECRET
- All endpoints enforce user data isolation by checking user_id
- Rate limiting prevents API abuse
- Input validation prevents injection attacks
- All database queries are parameterized to prevent SQL injection

## Architecture

The application follows a layered architecture:

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
# Quickstart Guide: Todo Backend API

## Prerequisites

- Python 3.11+
- PostgreSQL (or Neon Serverless PostgreSQL account)
- Better Auth configured for your frontend
- pip package manager
- Virtual environment tool (venv, conda, etc.)

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the backend root:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your_better_auth_secret_key
JWT_ALGORITHM=HS256
ENVIRONMENT=development
```

### 5. Database Setup
```bash
# Initialize the database (SQLModel creates tables automatically)
python -c "from src.database.config import engine, create_db_and_tables; create_db_and_tables()"
```

## Running the API

### Development Mode
```bash
# Using uvicorn directly
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or using the run script if available
python -m src.main
```

### Production Mode
```bash
# Using gunicorn (install with pip install "gunicorn[standard]")
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Endpoints

### Authentication
All endpoints require a valid JWT token from Better Auth in the Authorization header:
```
Authorization: Bearer <jwt_token_here>
```

### Task Operations

#### Create Task
```
POST /api/tasks
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Sample Task",
  "description": "Task description (optional)",
  "completed": false
}
```

#### Get All Tasks
```
GET /api/tasks?[status=all|pending|completed]&[sort=created_at|title]&[order=asc|desc]&[page=1]&[limit=10]
Authorization: Bearer <token>
```

#### Get Specific Task
```
GET /api/tasks/{task_id}
Authorization: Bearer <token>
```

#### Update Task
```
PUT /api/tasks/{task_id}
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Updated Task Title",
  "description": "Updated description",
  "completed": true
}
```

#### Delete Task
```
DELETE /api/tasks/{task_id}
Authorization: Bearer <token>
```

## Testing

### Run Unit Tests
```bash
pytest tests/unit/
```

### Run Integration Tests
```bash
pytest tests/integration/
```

### Run All Tests
```bash
pytest tests/
```

## Docker Deployment

### Build Image
```bash
docker build -t todo-backend .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e BETTER_AUTH_SECRET=... \
  -e ENVIRONMENT=production \
  todo-backend
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DATABASE_URL | PostgreSQL connection string | Yes | - |
| BETTER_AUTH_SECRET | Secret key for JWT verification | Yes | - |
| JWT_ALGORITHM | Algorithm for JWT verification | No | HS256 |
| ENVIRONMENT | Environment mode | No | development |
| ACCESS_TOKEN_EXPIRE_MINUTES | JWT expiration time | No | 30 |
| DEBUG | Enable debug mode | No | False |

## Health Checks

### API Health Endpoint
```
GET /health
```
Returns: `{"status": "healthy", "timestamp": "ISO8601"}`

### Database Connection
The health endpoint also verifies database connectivity.

## Troubleshooting

### Common Issues

1. **JWT Token Validation Failures**
   - Verify BETTER_AUTH_SECRET matches Better Auth configuration
   - Check token format: `Bearer <valid_jwt_token>`
   - Ensure token hasn't expired

2. **Database Connection Issues**
   - Verify DATABASE_URL format and credentials
   - Check PostgreSQL server is running and accessible
   - Confirm database exists and user has proper permissions

3. **User Isolation Not Working**
   - Ensure JWT middleware is properly extracting user_id
   - Verify all queries filter by authenticated user's ID
   - Check that user_id in URL path matches authenticated user

4. **CORS Issues**
   - Configure CORS middleware for frontend domain
   - Ensure Authorization header is allowed in requests

### Logging
- Logs are output to stdout by default
- Set LOG_LEVEL environment variable for verbosity
- Production deployments should use centralized logging

## Development Workflow

1. Activate virtual environment
2. Make code changes
3. Run tests: `pytest tests/`
4. Format code: `black . && isort .`
5. Start server: `uvicorn src.main:app --reload`
6. Test endpoints via Swagger UI at `/docs`

## Security Best Practices

- Never expose secrets in code or commit to version control
- Use HTTPS in production
- Implement rate limiting for public endpoints
- Sanitize all user inputs
- Regular security audits of dependencies
- Keep dependencies updated
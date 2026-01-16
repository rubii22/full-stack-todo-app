# Data Model: Todo Backend API

## Entity Definitions

### User Entity
- **Name**: User
- **Fields**:
  - `id` (UUID/String): Unique identifier from Better Auth
  - `email` (String): User's email address from Better Auth
  - `name` (String, optional): User's display name
  - `created_at` (DateTime): Account creation timestamp
  - `updated_at` (DateTime): Last update timestamp
- **Relationships**:
  - One-to-many with Task entity (via tasks.user_id foreign key)
- **Notes**: Managed by Better Auth, referenced by tasks via user_id

### Task Entity
- **Name**: Task
- **Fields**:
  - `id` (Integer): Auto-incrementing primary key
  - `user_id` (String/UUID): Foreign key to User.id from Better Auth
  - `title` (String): Task title (required, max 255 chars)
  - `description` (String, optional): Task description (max 1000 chars)
  - `completed` (Boolean): Task completion status (default: False)
  - `created_at` (DateTime): Task creation timestamp (auto-generated)
  - `updated_at` (DateTime): Task last update timestamp (auto-generated)
- **Relationships**:
  - Many-to-one with User entity (via user_id foreign key)
- **Validation Rules**:
  - Title is required and must be 1-255 characters
  - Description, if provided, must be 0-1000 characters
  - user_id must reference a valid user in the system
  - completed defaults to False if not specified

## Database Schema

### tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

## Relationships
- **User → Task**: One-to-many (one user can have many tasks)
- **Task → User**: Many-to-one (each task belongs to one user)
- **Referential Integrity**: CASCADE delete on user deletion removes associated tasks
- **Constraints**:
  - NOT NULL constraints on user_id and title
  - Foreign key constraint ensuring user_id references valid user

## State Transitions
- **Task Creation**: New task with completed=False, created_at set to current time
- **Task Update**:
  - Title/description can be modified
  - Completed status can be toggled
  - updated_at automatically updated to current time
- **Task Deletion**: Row removed from database (handled by CASCADE if user deleted)

## Validation Rules
- **Task Creation**:
  - Title must be 1-255 characters
  - user_id must exist in users table
  - completed defaults to False if not provided
- **Task Updates**:
  - user_id cannot be changed (enforced by API, not DB)
  - Title must remain 1-255 characters if updated
  - Only tasks belonging to authenticated user can be modified
- **Access Control**:
  - Users can only access tasks where user_id matches their authenticated ID
  - Attempting to access another user's task returns 404/403

## Indexing Strategy
- **Primary Index**: id (automatically indexed as primary key)
- **User Access Index**: idx_tasks_user_id for efficient user-specific queries
- **Filtering Index**: idx_tasks_completed for status-based queries
- **Combined Index**: idx_tasks_user_completed for common user+status queries

## Audit Trail
- **Creation**: created_at timestamp automatically set on INSERT
- **Updates**: updated_at timestamp automatically updated on any modification
- **Access**: User ID from JWT token logged for access control verification
- **Deletion**: Tasks removed with user account (CASCADE) or individually via API

## Constraints Summary
- **Primary Key**: id (unique, non-null)
- **Foreign Key**: user_id references users(id)
- **Required Fields**: user_id, title
- **Default Values**: completed=False, created_at/CURRENT_TIMESTAMP
- **Data Types**: Enforced by column definitions
- **Length Limits**: Title (255), Description (1000)
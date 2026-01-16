<!-- SYNC IMPACT REPORT:
Version change: N/A -> 1.0.0
Modified principles: None (new constitution)
Added sections: All sections based on user input
Removed sections: None
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-Driven Development
Spec-driven development using Claude Code and Spec-Kit Plus for structured implementation. All implementation must follow the defined specifications and utilize the established tools for consistent delivery.

### Multi-User Security
Multi-user security with user isolation and authentication to ensure data privacy. All user data must be properly isolated and protected through authentication mechanisms.

### Responsive and Modern Frontend
Responsiveness and modernity in frontend for intuitive user experience. The frontend must provide a modern, responsive interface that delivers an intuitive experience to users.

### Persistent and Scalable Storage
Persistence and scalability through serverless PostgreSQL database. Database operations must be designed to leverage the scalable nature of serverless infrastructure.

### Cross-Stack Consistency
Cross-stack consistency between frontend and backend for seamless integration. Both frontend and backend components must maintain consistent interfaces and behaviors.

## Key Standards

All features must reference and adhere to specs in /specs/ directory (e.g., @specs/features/task-crud.md). API endpoints must be RESTful, secured with JWT tokens, and filtered by authenticated user ID. Database operations must use SQLModel ORM with schema as defined in /specs/database/schema.md. Authentication must integrate Better Auth on frontend with FastAPI verification on backend using shared secret. Code patterns must follow CLAUDE.md guidelines: root for overview, frontend for Next.js patterns, backend for FastAPI conventions. Testing must enforce user-specific data access, token validation, and error handling (e.g., 401 Unauthorized).

## Constraints

Tech stack: Next.js 16+ (App Router) for frontend, Python FastAPI for backend, SQLModel ORM, Neon Serverless PostgreSQL database, Better Auth for authentication. Monorepo structure: hackathon-todo/ with .spec-kit/, specs/, frontend/, backend/, CLAUDE.md files, docker-compose.yml. Phases: Focus on Phase II (web app with task-crud and authentication); prepare for Phase III (chatbot). No deviations from specified endpoints or security model; all tasks user-owned. Environment variables: Use BETTER_AUTH_SECRET for JWT; DATABASE_URL for DB connection. Development workflow: Write/update specs first, then implement via Claude Code references.

## Governance

All implementation must adhere to the specified architecture and technology stack. Changes to core architecture require explicit approval and documentation. All code must reference and comply with the established specs and follow the development workflow outlined in the constitution.

**Version**: 1.0.0 | **Ratified**: 2026-01-15 | **Last Amended**: 2026-01-15
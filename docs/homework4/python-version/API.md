# TODO REST API - Complete API Reference (Python FastAPI)

## Overview

This document defines the complete API contract for the TODO REST API, including all endpoint specifications, authentication, request/response schemas, validation rules, and security guidelines.

**Base URL:** `http://localhost:8000/api/v1` (or your deployed server URL)

**Content-Type:** `application/json`

---

## Table of Contents

- [Data Models](#data-models)
- [Health Check](#health-check)
- [Authentication](#authentication)
- [List Endpoints](#list-endpoints)
- [Task Endpoints](#task-endpoints)
- [Error Responses](#error-responses)
- [Security Guidelines](#security-guidelines)

---

## Data Models

### User

```json
{
  "id": "string (UUID v4)",
  "username": "string (3-50 chars, unique)",
  "email": "string (valid email, unique)",
  "createdAt": "string (ISO 8601 datetime)",
  "updatedAt": "string (ISO 8601 datetime, optional)"
}
```

**Note:** Passwords are never returned in responses.

### List

```json
{
  "id": "string (UUID v4)",
  "title": "string (required, max 255 chars)",
  "description": "string (optional, max 1000 chars)",
  "createdAt": "string (ISO 8601 datetime)",
  "updatedAt": "string (ISO 8601 datetime, optional)"
}
```

### Task

```json
{
  "id": "string (UUID v4)",
  "listId": "string (UUID v4)",
  "title": "string (required, max 255 chars)",
  "description": "string (optional, max 2000 chars)",
  "completed": "boolean (default: false)",
  "priority": "string (enum: 'low', 'medium', 'high')",
  "categories": "array of strings (max 10 items, each max 50 chars)",
  "dueDate": "string (ISO 8601 datetime, optional)",
  "createdAt": "string (ISO 8601 datetime)",
  "updatedAt": "string (ISO 8601 datetime, optional)"
}
```

---

## Health Check

### GET /api/v1/health

Check the health and status of the API and its dependencies.

**Authentication:** Not required

**Success Response (200):**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-01T15:03:33.232819Z",
  "service": "TODO REST API",
  "version": "1.0.0",
  "checks": {
    "database": {
      "status": "healthy",
      "message": "Database connection successful"
    },
    "python": {
      "status": "healthy",
      "version": "3.11"
    },
    "disk": {
      "status": "healthy",
      "free_space_mb": 146645.1,
      "used_percent": 6.8
    },
    "memory": {
      "status": "healthy",
      "memory_usage_mb": 13352,
      "memory_available_mb": 3032
    }
  }
}
```

**Status Values:**
- `healthy`: All systems operational
- `warning`: System is operational but has warnings
- `unhealthy`: Critical issue detected (returns 503 status code)

---

## Authentication

The API uses **JWT (JSON Web Token)** for authentication:
- Passwords are hashed with **Argon2** (no length limits)
- Tokens expire after **1 hour** (configurable)
- Tokens are sent as `Authorization: Bearer <token>` header
- Tokens are blacklisted on logout to prevent reuse

### POST /api/v1/auth/signup

Create a new user account.

**Request Body:**
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "password123"
}
```

**Validation Rules:**
- `username`: 3-50 characters, unique, alphanumeric (underscores/hyphens allowed)
- `email`: Valid email format, unique
- `password`: Minimum 8 characters

**Success Response (201):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "a1b2c3d4-...",
    "username": "alice",
    "email": "alice@example.com",
    "createdAt": "2025-12-01T10:00:00Z"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Validation error
- `409 Conflict` - Username or email already exists
- `422 Unprocessable Entity` - Invalid input format
- `500 Internal Server Error` - Server error

---

### POST /api/v1/auth/login

Authenticate and receive a JWT token.

**Request Body:**
```json
{
  "username": "alice",
  "password": "password123"
}
```

**Success Response (200):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "a1b2c3d4-...",
    "username": "alice",
    "email": "alice@example.com",
    "createdAt": "2025-12-01T10:00:00Z"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid username or password
- `422 Unprocessable Entity` - Invalid input format
- `500 Internal Server Error` - Server error

---

### GET /api/v1/users/profile

Get current user profile (requires authentication).

**Headers Required:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Success Response (200):**
```json
{
  "id": "a1b2c3d4-...",
  "username": "alice",
  "email": "alice@example.com",
  "createdAt": "2025-12-01T10:00:00Z",
  "updatedAt": null
}
```

**Error Responses:**
- `401 Unauthorized` - Missing, invalid, expired, or blacklisted token
- `404 Not Found` - User not found
- `500 Internal Server Error` - Server error

---

### POST /api/v1/auth/logout

Logout and blacklist the current token (requires authentication).

**Headers Required:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Success Response (204):**
- No content
- Token is added to blacklist and can no longer be used

---

## List Endpoints

### GET /api/v1/lists

Retrieve all lists.

**Response (200 OK):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Groceries",
    "description": "Weekly shopping list",
    "createdAt": "2025-12-01T10:00:00Z",
    "updatedAt": null
  }
]
```

---

### GET /api/v1/lists/{id}

Retrieve a single list by ID.

**URL Parameters:** `id` (UUID v4)

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Groceries",
  "description": "Weekly shopping list",
  "createdAt": "2025-12-01T10:00:00Z",
  "updatedAt": null
}
```

**Error Responses:**
- `400 Bad Request` - Invalid UUID format
- `404 Not Found` - List not found

---

### POST /api/v1/lists

Create a new list.

**Request Body:**
```json
{
  "title": "Groceries",
  "description": "Weekly shopping list"
}
```

**Validation Rules:**
- `title`: Required, string, 1-255 characters, cannot be only whitespace
- `description`: Optional, string, max 1000 characters

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Groceries",
  "description": "Weekly shopping list",
  "createdAt": "2025-12-01T10:00:00Z",
  "updatedAt": null
}
```

---

### PATCH /api/v1/lists/{id}

Update an existing list.

**URL Parameters:** `id` (UUID v4)

**Request Body (all fields optional):**
```json
{
  "title": "Updated Groceries",
  "description": "Updated description"
}
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated Groceries",
  "description": "Updated description",
  "createdAt": "2025-12-01T10:00:00Z",
  "updatedAt": "2025-12-01T11:00:00Z"
}
```

---

### DELETE /api/v1/lists/{id}

Delete a list and all associated tasks.

**URL Parameters:** `id` (UUID v4)

**Response (204 No Content):**
- Empty body

---

## Task Endpoints

### GET /api/v1/lists/{listId}/tasks

Retrieve all tasks in a specific list.

**URL Parameters:** `listId` (UUID v4)

**Response (200 OK):**
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "listId": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy milk",
    "description": "Get organic milk from the store",
    "completed": false,
    "priority": "high",
    "categories": ["groceries", "dairy"],
    "dueDate": "2025-12-01T18:00:00Z",
    "createdAt": "2025-12-01T10:00:00Z",
    "updatedAt": null
  }
]
```

---

### GET /api/v1/tasks/{id}

Retrieve a single task by ID.

**URL Parameters:** `id` (UUID v4)

**Response (200 OK):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "listId": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy milk",
  "description": "Get organic milk from the store",
  "completed": false,
  "priority": "high",
  "categories": ["groceries", "dairy"],
  "dueDate": "2025-12-01T18:00:00Z",
  "createdAt": "2025-12-01T10:00:00Z",
  "updatedAt": null
}
```

---

### POST /api/v1/lists/{listId}/tasks

Create a new task in a specific list.

**URL Parameters:** `listId` (UUID v4)

**Request Body:**
```json
{
  "title": "Buy milk",
  "description": "Get organic milk from the store",
  "priority": "high",
  "dueDate": "2025-12-01T18:00:00Z",
  "categories": ["groceries", "dairy"]
}
```

**Validation Rules:**
- `title`: Required, string, 1-255 characters, cannot be only whitespace
- `description`: Optional, string, max 2000 characters
- `completed`: Optional, boolean (default: false)
- `dueDate`: Optional, valid ISO 8601 datetime string
- `priority`: Optional, enum ('low', 'medium', 'high')
- `categories`: Optional, array of strings, max 10 items, each max 50 characters

**Response (201 Created):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "listId": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy milk",
  "description": "Get organic milk from the store",
  "completed": false,
  "priority": "high",
  "categories": ["groceries", "dairy"],
  "dueDate": "2025-12-01T18:00:00Z",
  "createdAt": "2025-12-01T10:00:00Z",
  "updatedAt": null
}
```

---

### PATCH /api/v1/tasks/{id}

Update an existing task.

**URL Parameters:** `id` (UUID v4)

**Request Body (all fields optional):**
```json
{
  "title": "Buy organic milk",
  "completed": true,
  "priority": "medium"
}
```

**Response (200 OK):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "listId": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy organic milk",
  "description": "Get organic milk from the store",
  "completed": true,
  "priority": "medium",
  "categories": ["groceries", "dairy"],
  "dueDate": "2025-12-01T18:00:00Z",
  "createdAt": "2025-12-01T10:00:00Z",
  "updatedAt": "2025-12-01T11:00:00Z"
}
```

---

### DELETE /api/v1/tasks/{id}

Delete a task.

**URL Parameters:** `id` (UUID v4)

**Response (204 No Content):**
- Empty body

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error type",
  "code": "ERROR_CODE",
  "details": "Detailed error message or validation errors"
}
```

### Common HTTP Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Success with no response body
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict (duplicate)
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

### Validation Error Format

```json
{
  "error": "Validation error",
  "code": "VALIDATION_ERROR",
  "details": {
    "username": ["Username must be at least 3 characters"],
    "email": ["Invalid email format"]
  }
}
```

---

## Security Guidelines

### Authentication

1. **Use HTTPS** in production
2. **Store JWT tokens securely** (not in localStorage)
3. **Implement token refresh** for long sessions
4. **Validate tokens** on every protected request
5. **Logout properly** to blacklist tokens

### Password Security

1. **Minimum 8 characters** required
2. **Argon2 hashing** with secure parameters
3. **Never store plain text passwords**
4. **Never log passwords** in any form

### Input Validation

1. **Validate all inputs** with Pydantic schemas
2. **Sanitize user data** before processing
3. **Use parameterized queries** (automatic with SQLAlchemy)
4. **Validate UUIDs** for all ID parameters
5. **Enforce length limits** to prevent buffer overflows

### Rate Limiting

- **10 requests per second** per IP (configurable)
- Implemented at Nginx level
- Protects against abuse and DoS attacks

### Data Protection

1. **No sensitive data** in logs
2. **Generic error messages** in production
3. **Input sanitization** for all user data
4. **SQL injection prevention** via ORM
5. **XSS protection** via proper encoding

---

*This API contract ensures consistent, secure, and reliable communication between clients and the TODO REST API server.*
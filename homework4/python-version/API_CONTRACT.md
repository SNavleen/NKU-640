# TODO REST API - Complete API Contract

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
  "name": "string (required, max 255 chars)",
  "description": "string (optional, max 1000 chars)",
  "createdAt": "string (ISO 8601 datetime)",
  "updatedAt": "string (ISO 8601 datetime, optional)"
}
```

### Task

```json
{
  "id": "string (UUID v4)",
  "listId": "string (UUID v4, required)",
  "title": "string (required, max 255 chars)",
  "description": "string (optional, max 2000 chars)",
  "completed": "boolean (default: false)",
  "dueDate": "string (ISO 8601 datetime, optional)",
  "priority": "string (enum: 'low', 'medium', 'high', optional)",
  "categories": "array of strings (optional, max 10 items, each max 50 chars)",
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
  "timestamp": "2025-12-01T23:48:15Z",
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
      "free_space_mb": 5629.3,
      "used_percent": 27.41
    },
    "memory": {
      "status": "healthy",
      "memory_usage_mb": 256,
      "memory_available_mb": 1024
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
- Passwords are hashed with **bcrypt** (cost factor 12)
- Tokens expire after **1 hour** (configurable via `JWT_EXPIRY`)
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
    "createdAt": "2025-12-01T10:00:00Z",
    "updatedAt": null
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
    "createdAt": "2025-12-01T10:00:00Z",
    "updatedAt": null
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
    "name": "Groceries",
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
  "name": "Groceries",
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
  "name": "Groceries",
  "description": "Weekly shopping list"
}
```

**Validation Rules:**
- `name`: Required, string, 1-255 characters, cannot be only whitespace
- `description`: Optional, string, max 1000 characters

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Groceries",
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
  "name": "Updated Groceries",
  "description": "Updated description"
}
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Updated Groceries",
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
    "description": "2 liters, skim",
    "completed": false,
    "dueDate": "2025-12-07T18:00:00Z",
    "priority": "medium",
    "categories": ["groceries", "dairy"],
    "createdAt": "2025-12-01T10:05:00Z",
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
  "description": "2 liters, skim",
  "completed": false,
  "dueDate": "2025-12-07T18:00:00Z",
  "priority": "medium",
  "categories": ["groceries", "dairy"],
  "createdAt": "2025-12-01T10:05:00Z",
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
  "description": "2 liters, skim",
  "dueDate": "2025-12-07T18:00:00Z",
  "priority": "medium",
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
  "description": "2 liters, skim",
  "completed": false,
  "dueDate": "2025-12-07T18:00:00Z",
  "priority": "medium",
  "categories": ["groceries", "dairy"],
  "createdAt": "2025-12-01T10:05:00Z",
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
  "priority": "high"
}
```

**Response (200 OK):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "listId": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy organic milk",
  "description": "2 liters, skim",
  "completed": true,
  "dueDate": "2025-12-07T18:00:00Z",
  "priority": "high",
  "categories": ["groceries", "dairy"],
  "createdAt": "2025-12-01T10:05:00Z",
  "updatedAt": "2025-12-01T11:30:00Z"
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

All errors return JSON with the following format:

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {}
}
```

### HTTP Status Codes

- `200 OK` - Successful GET/PATCH request
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid request (validation error, malformed UUID, etc.)
- `401 Unauthorized` - Missing, invalid, expired, or blacklisted token
- `404 Not Found` - Resource not found
- `409 Conflict` - Duplicate username or email
- `422 Unprocessable Entity` - Request validation error
- `500 Internal Server Error` - Server/database error
- `503 Service Unavailable` - Health check failed

---

## Security Guidelines

### Authentication Security

1. **Password Hashing:**
   - Bcrypt with cost factor 12
   - Passwords never stored or returned in plain text

2. **JWT Token Management:**
   - Tokens expire after 1 hour
   - Signature verification with secret key
   - Token blacklisting on logout

3. **Token Blacklisting:**
   - Tokens added to blacklist on logout
   - Automatic cleanup of expired tokens
   - Prevents token reuse after logout

### Input Validation

1. **UUID Validation:**
   - All IDs must be valid UUID v4 format
   - Reject malformed UUIDs with `400 Bad Request`

2. **String Sanitization:**
   - Trim whitespace from all string inputs
   - Reject strings that are only whitespace when required
   - Enforce maximum length limits

3. **Data Type Validation:**
   - Validate JSON structure and data types using Pydantic
   - Reject invalid JSON with `422 Unprocessable Entity`

### Database Security

1. **SQL Injection Prevention:**
   - Use SQLAlchemy ORM for ALL database operations
   - Parameterized queries automatically prevent SQL injection

2. **Transaction Safety:**
   - Use transactions for operations affecting multiple tables
   - Implement proper rollback on errors

---

## Complete Authentication Flow Example

```bash
# 1. Sign up
SIGNUP=$(curl -s -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@test.com","password":"pass123456"}')

TOKEN=$(echo $SIGNUP | jq -r '.token')
echo "Token: $TOKEN"

# 2. Get profile (requires token)
curl -X GET http://localhost:8000/api/v1/users/profile \
  -H "Authorization: Bearer $TOKEN"

# 3. Logout (blacklist token)
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer $TOKEN"

# 4. Try to use token again (should fail with 401)
curl -X GET http://localhost:8000/api/v1/users/profile \
  -H "Authorization: Bearer $TOKEN"

# 5. Login to get new token
LOGIN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"pass123456"}')

NEW_TOKEN=$(echo $LOGIN | jq -r '.token')
echo "New token: $NEW_TOKEN"
```

---

## Endpoint Summary

| Method | Endpoint | Protected | Description |
|--------|----------|-----------|-------------|
| **Health** ||||
| GET | `/health` | No | Check API health |
| **Authentication** ||||
| POST | `/auth/signup` | No | Create account |
| POST | `/auth/login` | No | Authenticate user |
| POST | `/auth/logout` | Yes | Logout and blacklist token |
| GET | `/users/profile` | Yes | Get current user profile |
| **Lists** ||||
| GET | `/lists` | No | Get all lists |
| POST | `/lists` | No | Create list |
| GET | `/lists/{id}` | No | Get list by ID |
| PATCH | `/lists/{id}` | No | Update list |
| DELETE | `/lists/{id}` | No | Delete list |
| **Tasks** ||||
| GET | `/lists/{listId}/tasks` | No | Get tasks in list |
| POST | `/lists/{listId}/tasks` | No | Create task |
| GET | `/tasks/{id}` | No | Get task by ID |
| PATCH | `/tasks/{id}` | No | Update task |
| DELETE | `/tasks/{id}` | No | Delete task |

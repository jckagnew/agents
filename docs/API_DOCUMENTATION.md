# Design-First Software Factory - API Documentation

**Version:** 1.0.0
**Base URL:** `https://api.design-first.example.com/api/v1`
**WebSocket URL:** `wss://api.design-first.example.com/ws`

---

## Table of Contents

1. [Authentication](#authentication)
2. [Workflow Endpoints](#workflow-endpoints)
3. [Project Endpoints](#project-endpoints)
4. [Usage & Quota Endpoints](#usage--quota-endpoints)
5. [Health & Status Endpoints](#health--status-endpoints)
6. [WebSocket API](#websocket-api)
7. [Error Handling](#error-handling)
8. [Rate Limiting](#rate-limiting)
9. [Examples](#examples)

---

## Authentication

All API endpoints (except `/health` and `/stats`) require authentication via Bearer token.

### Headers

```http
Authorization: Bearer YOUR_SUPABASE_JWT_TOKEN
Content-Type: application/json
```

### Obtaining a Token

Use Supabase Auth to obtain a JWT token:

```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password',
});

const token = data.session.access_token;
```

---

## Workflow Endpoints

### POST /workflows

Start a new Design-First Software Factory workflow.

**Request:**

```http
POST /api/v1/workflows
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "projectName": "My Awesome App",
  "projectDescription": "A mobile app for tracking fitness goals",
  "targetPlatforms": ["ios", "android", "web"],
  "designPreferences": {
    "colorScheme": "light",
    "brandColors": ["#007AFF", "#5856D6"],
    "fontFamily": "System"
  },
  "metadata": {
    "category": "health",
    "priority": "high"
  }
}
```

**Response (202 Accepted):**

```json
{
  "message": "Workflow started",
  "project": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "My Awesome App",
    "status": "in_progress",
    "created_at": "2025-11-08T12:00:00Z"
  }
}
```

**Fields:**

- `projectName` (required): Name of the project
- `projectDescription` (required): Description of what the app should do
- `targetPlatforms` (optional): Array of `["ios", "android", "web"]`. Defaults to all three.
- `designPreferences` (optional): Design customization options
  - `colorScheme`: `"light"`, `"dark"`, or `"auto"`
  - `brandColors`: Array of hex color codes
  - `fontFamily`: Font family name
- `metadata` (optional): Additional metadata for the project

**Notes:**

- Workflow executes asynchronously
- Use WebSocket or polling to track progress
- Returns immediately with `202 Accepted` status

---

### GET /workflows/:projectId

Get the current status of a workflow.

**Request:**

```http
GET /api/v1/workflows/550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer YOUR_TOKEN
```

**Response (200 OK):**

```json
{
  "project": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user-123",
    "name": "My Awesome App",
    "description": "A mobile app for tracking fitness goals",
    "status": "in_progress",
    "target_platforms": ["ios", "android", "web"],
    "design_preferences": {
      "colorScheme": "light",
      "brandColors": ["#007AFF", "#5856D6"]
    },
    "created_at": "2025-11-08T12:00:00Z",
    "updated_at": "2025-11-08T12:05:30Z"
  },
  "workflow": {
    "id": "workflow-456",
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "current_phase": "design_generation",
    "status": "active",
    "phase_data": {
      "problem_deconstruction": {
        "status": "completed",
        "started_at": "2025-11-08T12:00:05Z",
        "completed_at": "2025-11-08T12:01:30Z",
        "result": { "..." }
      },
      "screen_mapping": {
        "status": "completed",
        "started_at": "2025-11-08T12:01:30Z",
        "completed_at": "2025-11-08T12:03:00Z"
      },
      "design_generation": {
        "status": "active",
        "started_at": "2025-11-08T12:03:00Z"
      }
    },
    "started_at": "2025-11-08T12:00:00Z"
  },
  "latestProgress": {
    "id": "progress-789",
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "phase": "design_generation",
    "step_name": "Generating component hierarchy",
    "step_index": 1,
    "total_steps": 6,
    "progress_pct": 33,
    "created_at": "2025-11-08T12:03:45Z"
  }
}
```

**Workflow Phases:**

1. `problem_deconstruction` - Transform idea into PRD
2. `screen_mapping` - Identify screens and navigation
3. `design_generation` - Generate visual designs
4. `stitch_iteration` - User feedback loop
5. `code_generation` - Generate Expo code
6. `code_review` - Validate code quality

**Workflow Statuses:**

- `active` - Currently executing
- `paused` - Temporarily paused
- `completed` - Successfully finished
- `failed` - Encountered an error

---

### POST /workflows/:projectId/pause

Pause a running workflow.

**Request:**

```http
POST /api/v1/workflows/550e8400-e29b-41d4-a716-446655440000/pause
Authorization: Bearer YOUR_TOKEN
```

**Response (200 OK):**

```json
{
  "message": "Workflow paused",
  "workflow": {
    "id": "workflow-456",
    "status": "paused",
    "current_phase": "design_generation"
  }
}
```

---

### POST /workflows/:projectId/resume

Resume a paused workflow.

**Request:**

```http
POST /api/v1/workflows/550e8400-e29b-41d4-a716-446655440000/resume
Authorization: Bearer YOUR_TOKEN
```

**Response (200 OK):**

```json
{
  "message": "Workflow resumed",
  "workflow": {
    "id": "workflow-456",
    "status": "active",
    "current_phase": "design_generation"
  }
}
```

---

## Project Endpoints

### GET /projects

List all projects for the authenticated user.

**Request:**

```http
GET /api/v1/projects?page=1&limit=20
Authorization: Bearer YOUR_TOKEN
```

**Query Parameters:**

- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20, max: 100)

**Response (200 OK):**

```json
{
  "projects": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "My Awesome App",
      "description": "A mobile app for tracking fitness goals",
      "status": "completed",
      "created_at": "2025-11-08T12:00:00Z",
      "completed_at": "2025-11-08T12:15:30Z"
    },
    {
      "id": "660e9511-f30c-52e5-b827-557766551111",
      "name": "E-commerce App",
      "description": "Online shopping platform",
      "status": "in_progress",
      "created_at": "2025-11-07T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 42,
    "totalPages": 3
  }
}
```

---

### GET /projects/:id

Get detailed information about a specific project.

**Request:**

```http
GET /api/v1/projects/550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer YOUR_TOKEN
```

**Response (200 OK):**

```json
{
  "project": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user-123",
    "name": "My Awesome App",
    "description": "A mobile app for tracking fitness goals",
    "status": "completed",
    "target_platforms": ["ios", "android", "web"],
    "design_preferences": {
      "colorScheme": "light",
      "brandColors": ["#007AFF", "#5856D6"],
      "fontFamily": "System"
    },
    "metadata": {
      "category": "health",
      "priority": "high"
    },
    "created_at": "2025-11-08T12:00:00Z",
    "updated_at": "2025-11-08T12:15:30Z",
    "completed_at": "2025-11-08T12:15:30Z"
  }
}
```

---

### GET /projects/:id/progress

Get detailed progress information for a project.

**Request:**

```http
GET /api/v1/projects/550e8400-e29b-41d4-a716-446655440000/progress
Authorization: Bearer YOUR_TOKEN
```

**Response (200 OK):**

```json
{
  "history": [
    {
      "id": "cp-1",
      "project_id": "550e8400-e29b-41d4-a716-446655440000",
      "phase": "problem_deconstruction",
      "step_name": "Analyzing user requirements",
      "step_index": 0,
      "total_steps": 5,
      "progress_pct": 20,
      "created_at": "2025-11-08T12:00:15Z"
    },
    {
      "id": "cp-2",
      "project_id": "550e8400-e29b-41d4-a716-446655440000",
      "phase": "problem_deconstruction",
      "step_name": "Extracting core features",
      "step_index": 1,
      "total_steps": 5,
      "progress_pct": 40,
      "created_at": "2025-11-08T12:00:30Z"
    }
  ],
  "latest": {
    "id": "cp-30",
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "phase": "code_review",
    "step_name": "Checking quality gates",
    "step_index": 5,
    "total_steps": 6,
    "progress_pct": 100,
    "created_at": "2025-11-08T12:15:20Z"
  },
  "overallProgress": 100
}
```

---

## Usage & Quota Endpoints

### GET /usage

Get current usage statistics and quota limits.

**Request:**

```http
GET /api/v1/usage
Authorization: Bearer YOUR_TOKEN
```

**Response (200 OK):**

```json
{
  "quota": {
    "tier": "pro",
    "limits": {
      "projects_per_month": 50,
      "ai_tokens_per_month": 5000000,
      "storage_gb": 10.0
    },
    "current_usage": {
      "projects": 12,
      "tokens": 1250000,
      "storage_gb": 2.5
    },
    "percentage_used": {
      "projects": 24,
      "tokens": 25,
      "storage": 25
    },
    "period_end": "2025-12-01T00:00:00Z"
  },
  "usage": {
    "id": "quota-123",
    "user_id": "user-123",
    "tier": "pro",
    "current_projects": 12,
    "current_tokens": 1250000,
    "current_storage_gb": 2.5,
    "period_start": "2025-11-01T00:00:00Z",
    "period_end": "2025-12-01T00:00:00Z"
  }
}
```

**Subscription Tiers:**

| Tier | Projects/mo | Tokens/mo | Storage |
|------|------------|-----------|---------|
| free | 3 | 100K | 1 GB |
| pro | 50 | 5M | 10 GB |
| enterprise | Unlimited | Unlimited | Unlimited |

---

## Health & Status Endpoints

### GET /health

Health check endpoint (no authentication required).

**Request:**

```http
GET /api/v1/health
```

**Response (200 OK):**

```json
{
  "status": "healthy",
  "timestamp": "2025-11-08T12:00:00Z",
  "services": {
    "database": "ok",
    "api": "ok"
  }
}
```

**Response (503 Service Unavailable):**

```json
{
  "status": "unhealthy",
  "error": "Database connection failed",
  "timestamp": "2025-11-08T12:00:00Z"
}
```

---

### GET /stats

Get system-wide statistics (no authentication required).

**Request:**

```http
GET /api/v1/stats
```

**Response (200 OK):**

```json
{
  "projects": {
    "total": 1542
  },
  "workflows": {
    "total": 1489,
    "active": 23
  },
  "timestamp": "2025-11-08T12:00:00Z"
}
```

---

## WebSocket API

Real-time progress updates via WebSocket.

### Connection

```javascript
const ws = new WebSocket('wss://api.design-first.example.com/ws?projectId=550e8400-e29b-41d4-a716-446655440000');

ws.onopen = () => {
  console.log('Connected to progress updates');
};

ws.onmessage = (event) => {
  const progressEvent = JSON.parse(event.data);
  console.log('Progress update:', progressEvent);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected from progress updates');
};
```

### Progress Event Format

```json
{
  "type": "phase_progress",
  "projectId": "550e8400-e29b-41d4-a716-446655440000",
  "phase": "design_generation",
  "progress": 50,
  "step": "Applying platform-specific styles",
  "message": "Applying platform-specific styles",
  "metadata": {
    "platform": "ios"
  },
  "timestamp": "2025-11-08T12:05:30.123Z"
}
```

### Event Types

- `phase_start` - New phase started
- `phase_progress` - Progress within a phase
- `phase_complete` - Phase completed
- `phase_error` - Error occurred in phase
- `workflow_complete` - Entire workflow completed

---

## Error Handling

### Error Response Format

```json
{
  "error": "Error description",
  "code": "ERROR_CODE",
  "details": {
    "field": "projectName",
    "message": "Project name is required"
  }
}
```

### Common HTTP Status Codes

- `200 OK` - Request succeeded
- `202 Accepted` - Request accepted for async processing
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Missing or invalid authentication token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service temporarily unavailable

### Common Error Codes

- `MISSING_AUTH_TOKEN` - No authorization header provided
- `INVALID_AUTH_TOKEN` - Token is invalid or expired
- `PROJECT_NOT_FOUND` - Project does not exist or user doesn't have access
- `WORKFLOW_NOT_FOUND` - Workflow not found for project
- `QUOTA_EXCEEDED` - User has exceeded their quota limits
- `VALIDATION_ERROR` - Request validation failed
- `RATE_LIMIT_EXCEEDED` - Too many requests

---

## Rate Limiting

- **Limit:** 100 requests per 15 minutes per IP address
- **Headers:**
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Remaining requests in current window
  - `X-RateLimit-Reset`: Unix timestamp when limit resets

### Rate Limit Response (429)

```json
{
  "error": "Too many requests from this IP, please try again later.",
  "retryAfter": 900
}
```

---

## Examples

### Complete Workflow Example (JavaScript)

```javascript
import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_ANON_KEY = 'your-anon-key';
const API_BASE_URL = 'https://api.design-first.example.com/api/v1';

// 1. Authenticate with Supabase
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

const { data: authData } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password',
});

const token = authData.session.access_token;

// 2. Start a workflow
const response = await fetch(`${API_BASE_URL}/workflows`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    projectName: 'Fitness Tracker',
    projectDescription: 'A mobile app to track workouts and nutrition',
    targetPlatforms: ['ios', 'android'],
    designPreferences: {
      colorScheme: 'light',
      brandColors: ['#FF6B6B', '#4ECDC4'],
    },
  }),
});

const { project } = await response.json();
const projectId = project.id;

console.log('Workflow started for project:', projectId);

// 3. Connect to WebSocket for real-time updates
const ws = new WebSocket(`wss://api.design-first.example.com/ws?projectId=${projectId}`);

ws.onmessage = (event) => {
  const progressEvent = JSON.parse(event.data);

  console.log(`[${progressEvent.phase}] ${progressEvent.step || ''} - ${progressEvent.progress}%`);

  if (progressEvent.type === 'workflow_complete') {
    console.log('Workflow completed!');
    ws.close();

    // 4. Fetch final results
    fetchResults(projectId, token);
  }
};

// 5. Fetch results
async function fetchResults(projectId, token) {
  const response = await fetch(`${API_BASE_URL}/workflows/${projectId}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  const { project, workflow } = await response.json();

  console.log('Final project status:', project.status);
  console.log('Generated code available at:', project.output_path);
}
```

### Polling Example (Alternative to WebSocket)

```javascript
async function pollWorkflowStatus(projectId, token) {
  const interval = 5000; // Poll every 5 seconds

  const checkStatus = async () => {
    const response = await fetch(`${API_BASE_URL}/workflows/${projectId}`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    const { workflow, latestProgress } = await response.json();

    console.log(`Current phase: ${workflow.current_phase}`);
    console.log(`Progress: ${latestProgress.progress_pct}%`);

    if (workflow.status === 'completed') {
      console.log('Workflow completed!');
      return true;
    } else if (workflow.status === 'failed') {
      console.error('Workflow failed:', workflow.error_message);
      return true;
    }

    return false;
  };

  while (!(await checkStatus())) {
    await new Promise(resolve => setTimeout(resolve, interval));
  }
}

// Usage
await pollWorkflowStatus(projectId, token);
```

---

## Support

For API support, please contact:

- **Email:** api-support@design-first.example.com
- **Documentation:** https://docs.design-first.example.com
- **GitHub Issues:** https://github.com/design-first/software-factory/issues

---

**Last Updated:** November 8, 2025
**API Version:** 1.0.0

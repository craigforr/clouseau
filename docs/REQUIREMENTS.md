# Clouseau Requirements

This document tracks project requirements, standards, and acceptance criteria.

## Test Coverage Requirements

| Tier | Target | Rationale |
|------|--------|-----------|
| **Backend API** | 100% | Critical path - all API endpoints must be fully tested |
| **Backend Services** | 95% | Core business logic requires high coverage |
| **CLI** | 95% | User-facing commands need comprehensive testing |
| **Frontend** | 85% | UI components with reasonable coverage |

### Coverage Enforcement

- **Backend:** Configured in `backend/pyproject.toml` via pytest-cov
- **Frontend:** Configured in `frontend/vite.config.ts` via v8 provider
- **CLI:** Configured in `cli/vitest.config.ts` (when implemented)

### Current Status

| Tier | Statements | Branches | Functions | Lines | Status |
|------|------------|----------|-----------|-------|--------|
| Backend | TBD | TBD | TBD | TBD | ⏳ In Progress |
| Frontend | 100% | 94% | 100% | 100% | ✅ Exceeds Target |
| CLI | - | - | - | - | 🔲 Not Started |

## Code Quality Standards

### TypeScript/JavaScript
- Strict TypeScript enabled
- ESLint with React hooks plugin
- No `any` types without justification

### Python
- Type hints required for all public functions
- MyPy strict mode
- Ruff for linting and formatting

## API Design Standards

### REST Conventions
- Use plural nouns for resources (`/sessions`, `/conversations`)
- Nested routes for relationships (`/sessions/{id}/conversations`)
- Standard HTTP methods (GET, POST, PUT, DELETE)
- Consistent error response format

### Response Format
```json
{
  "id": 1,
  "field_name": "value",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Error Format
```json
{
  "detail": "Error message",
  "code": "ERROR_CODE"
}
```

## Data Model Requirements

### Sessions
- `id`: Primary key (integer)
- `name`: Required, max 255 chars
- `description`: Optional text
- `created_at`: Auto-set timestamp
- `updated_at`: Auto-updated timestamp

### Conversations
- `id`: Primary key (integer)
- `session_id`: Foreign key to sessions
- `title`: Required, max 255 chars
- `created_at`: Auto-set timestamp
- `updated_at`: Auto-updated timestamp

### Exchanges
- `id`: Primary key (integer)
- `conversation_id`: Foreign key to conversations
- `user_message`: Required text
- `assistant_message`: Required text
- `model`: Optional, max 100 chars
- `input_tokens`: Optional integer
- `output_tokens`: Optional integer
- `created_at`: Auto-set timestamp

## Frontend Requirements

### State Management
- React Context for global selection state
- Custom hooks for data fetching
- No external state management libraries required

### Component Standards
- Functional components only
- TypeScript interfaces for all props
- Loading, error, and empty states for async components

### Styling
- Tailwind CSS for styling
- Dark mode support via `dark:` variants
- Responsive design (mobile-first)

## Security Requirements

- No secrets in code or git history
- Environment variables for configuration
- Input validation on all API endpoints
- SQL injection prevention via parameterized queries

## Performance Requirements

- API response time < 200ms for list endpoints
- Frontend initial load < 3 seconds
- Database queries use appropriate indexes

## Browser Support

- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)

---

*Last updated: 2025-01-21*

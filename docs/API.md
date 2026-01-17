# Clouseau API Documentation

## Overview

The Clouseau API provides endpoints for managing LLM interaction sessions, conversations, and exchanges.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

TBD

## Endpoints

### Sessions

- `GET /sessions` - List all sessions
- `POST /sessions` - Create a new session
- `GET /sessions/{id}` - Get session details
- `DELETE /sessions/{id}` - Delete a session

### Conversations

- `GET /conversations` - List conversations
- `POST /conversations` - Create a conversation
- `GET /conversations/{id}` - Get conversation details

### Exchanges

- `GET /exchanges` - List exchanges
- `POST /exchanges` - Create an exchange
- `GET /exchanges/{id}` - Get exchange details

### Search

- `GET /search` - Search conversations and exchanges

## Response Format

All responses follow this format:

```json
{
  "data": {},
  "meta": {
    "page": 1,
    "total": 100
  }
}
```

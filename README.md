# Clouseau

An inspector for LLM interactions written in Python, TypeScript, and React.

## Overview

Clouseau is a comprehensive observability tool for tracking, analyzing, and managing conversations with Large Language Models. It provides:

- Session and conversation management
- Real-time context window tracking
- Multi-provider LLM support
- Full-text search across conversations
- Web UI and CLI interfaces

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- uv (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/craigforr/clouseau.git
cd clouseau

# Run setup script
./scripts/setup_dev.sh
```

### Running

```bash
# Start the backend server
cd backend
uv run uvicorn app.main:app --reload

# Start the web frontend (in another terminal)
cd frontend
npm run dev

# Or use the CLI
cd cli
npm run build
clou chat
```

## Project Structure

```
clouseau/
├── backend/          # Python FastAPI backend
├── frontend/         # React web interface
├── cli/              # React Ink CLI
├── docs/             # Documentation
└── scripts/          # Setup and utility scripts
```

## Documentation

- [API Documentation](docs/API.md)
- [Search Syntax](docs/SEARCH_SYNTAX.md)
- [Configuration Guide](docs/CONFIGURATION.md)

## Development

See [DEVELOPER.md](DEVELOPER.md) for development guidelines.

### Testing

```bash
# Backend tests
cd backend
uv run pytest --cov=app

# Frontend tests
cd frontend
npm test

# CLI tests
cd cli
npm test
```

## License

MIT License - see [LICENSE](LICENSE) for details.

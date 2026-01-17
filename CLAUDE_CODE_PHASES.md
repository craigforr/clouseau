# Clouseau Development Phases for Claude Code

## Overview
This document outlines the development phases for Clouseau. Each phase should be completed with full test coverage before moving to the next.

## Phase 1: Foundation (Week 1)

**GitHub Issues:** #1-10

### Tasks:
1. **Issue #1:** Initialize project structure
   - Create directory structure for backend, frontend, CLI
   - Set up .gitignore files
   - Create README.md skeleton
   
2. **Issue #2:** Configure testing frameworks
   - Backend: pytest with pytest-cov
   - Frontend: Jest with React Testing Library
   - CLI: Jest with Ink testing utilities
   - Set up coverage reporting
   
3. **Issue #3:** Set up Python environment with uv
   - Install uv
   - Create pyproject.toml
   - Set up virtual environment
   - Configure dev dependencies
   
4. **Issue #4:** Database models with migrations
   - SQLAlchemy models (Session, Conversation, Exchange)
   - Alembic configuration
   - Initial migration
   - 100% test coverage for models
   
5. **Issue #5:** Configuration parsers
   - config.yaml parser (LLM providers)
   - settings.yaml parser (CLI/GUI settings)
   - Environment variable substitution
   - Pydantic schemas for validation
   - 95%+ test coverage
   
6. **Issue #6:** LLM provider base class
   - Abstract base class
   - Type definitions
   - Mock provider for testing
   - 100% test coverage

**Deliverables:**
- Complete project structure
- All testing frameworks operational
- Database models with migrations
- Configuration system working
- LLM provider interface defined

**Coverage Requirements:**
- Backend: 95%+
- All tests passing

---

## Phase 2: Core Backend (Week 2)

**GitHub Issues:** #11-25

### Tasks:
7. **Issue #11:** Session management API
   - CRUD endpoints for sessions
   - Auto-save functionality
   - Session name generation
   - 100% API coverage
   
8. **Issue #12:** Conversation management API
   - CRUD endpoints for conversations
   - Link to sessions
   - Auto-save functionality
   - 100% API coverage
   
9. **Issue #13:** Exchange persistence
   - Exchange creation endpoint
   - Automatic context snapshot
   - Automatic API log capture
   - Token counting
   - 100% API coverage
   
10. **Issue #14:** Search query parser
    - Parse search syntax (date, model, content filters)
    - Query builder
    - 95% coverage
    
11. **Issue #15:** Search executor
    - FTS5 integration
    - Fuzzy matching
    - Result ranking
    - 95% coverage
    
12. **Issue #16:** Search API endpoints
    - Search endpoint
    - Advanced query support
    - Result pagination
    - 100% API coverage
    
13. **Issue #17:** Anthropic LLM provider
    - Implementation of base class
    - Streaming support
    - Error handling
    - 95% coverage (with mocking)
    
14. **Issue #18:** Export functionality
    - YAML export
    - JSON export
    - Session and conversation export
    - 95% coverage
    
15. **Issue #19:** Import functionality
    - YAML import
    - JSON import
    - Validation
    - GUID conflict resolution
    - 95% coverage
    
16. **Issue #20:** Configuration API endpoints
    - Get settings
    - Update settings
    - Validate settings
    - 100% API coverage

**Deliverables:**
- Fully functional backend API
- Session/conversation/exchange management
- Search functionality
- Import/export working
- Anthropic provider implemented

**Coverage Requirements:**
- API: 100%
- Backend: 95%+

---

## Phase 3: Web Interface (Week 3)

**GitHub Issues:** #26-45

### Tasks:
17. **Issue #26:** React app setup with TypeScript
    - Create React app structure
    - Configure TypeScript
    - Set up Tailwind CSS
    - Configure testing
    
18. **Issue #27:** Theme detection and switching
    - OS theme detection
    - Theme context provider
    - Theme toggle component
    - 85% coverage
    
19. **Issue #28:** API client service
    - Axios configuration
    - WebSocket client
    - Type definitions
    - 85% coverage
    
20. **Issue #29:** Session browser component
    - Session list display
    - Session metadata
    - Create/rename/delete
    - 85% coverage
    
21. **Issue #30:** Search interface component
    - Search input with autocomplete
    - Query builder UI
    - Result display
    - 85% coverage
    
22. **Issue #31:** Chat view component
    - Message display
    - Input field
    - Send message
    - 85% coverage
    
23. **Issue #32:** Context tab component
    - Syntax highlighting
    - Format JSON/YAML
    - Copy button
    - 85% coverage
    
24. **Issue #33:** API Log tab component
    - Request/response display
    - Timing information
    - Error display
    - 85% coverage
    
25. **Issue #34:** Markdown tab component
    - Markdown rendering
    - Copy to clipboard
    - Metadata inclusion
    - 85% coverage
    
26. **Issue #35:** Context usage visualization
    - Progress bar component
    - Token statistics
    - Model information
    - Color coding
    - 85% coverage
    
27. **Issue #36:** Exchange navigation
    - Forward/backward buttons
    - Keyboard shortcuts
    - Position indicator
    - 85% coverage
    
28. **Issue #37:** Settings panel
    - Form controls
    - Validation
    - Save/cancel
    - 85% coverage
    
29. **Issue #38:** WebSocket streaming integration
    - Streaming response display
    - Progress indication
    - Error handling
    - 85% coverage

**Deliverables:**
- Fully functional web interface
- All four tabs working
- Theme system operational
- Search interface complete
- Settings management

**Coverage Requirements:**
- Frontend: 85%+

---

## Phase 4: CLI Interface (Week 4)

**GitHub Issues:** #46-65

### Tasks:
30. **Issue #46:** TypeScript + React Ink setup
    - Project structure
    - Dependencies
    - Build configuration
    - Testing setup
    
31. **Issue #47:** CLI entry point and command parsing
    - Main CLI structure
    - Command routing
    - Help system
    - 95% coverage
    
32. **Issue #48:** Interactive chat interface
    - REPL implementation
    - Message input
    - Response streaming
    - 95% coverage
    
33. **Issue #49:** Chat view component (Ink)
    - Message display
    - Formatting
    - Scrolling
    - 95% coverage
    
34. **Issue #50:** Context panel component
    - Toggle visibility
    - Syntax highlighting
    - Box drawing
    - 95% coverage
    
35. **Issue #51:** Stats panel component
    - Token display
    - Model information
    - Color coding
    - 95% coverage
    
36. **Issue #52:** API Log panel component
    - Request/response display
    - Timing info
    - Error handling
    - 95% coverage
    
37. **Issue #53:** Status bar component
    - Session info
    - Model display
    - Token usage
    - Panel indicators
    - 95% coverage
    
38. **Issue #54:** Hotkey system
    - Key binding
    - Panel toggles
    - Help overlay
    - 95% coverage
    
39. **Issue #55:** Color scheme implementation
    - Dark mode colors
    - Monochrome fallback
    - Theme detection
    - 95% coverage
    
40. **Issue #56:** Configuration TUI
    - Interactive settings editor
    - Arrow key navigation
    - Value editing
    - 95% coverage
    
41. **Issue #57:** Session management commands
    - List sessions
    - Create/open session
    - Export/import
    - 95% coverage
    
42. **Issue #58:** Search command
    - Query parsing
    - Result display
    - Interactive selection
    - 95% coverage
    
43. **Issue #59:** History navigation
    - Exchange browsing
    - Jump to exchange
    - 95% coverage
    
44. **Issue #60:** Model switching
    - List models
    - Switch provider
    - 95% coverage

**Deliverables:**
- Fully functional CLI
- All panels and hotkeys working
- Configuration TUI complete
- Search functionality
- Color scheme with fallback

**Coverage Requirements:**
- CLI: 95%+

---

## Phase 5: Additional LLM Providers (Week 5)

**GitHub Issues:** #66-80

### Tasks:
45. **Issue #66:** OpenAI provider implementation
    - Base class implementation
    - Chat completions API
    - Streaming support
    - 95% coverage
    
46. **Issue #67:** Ollama provider implementation
    - Local endpoint support
    - Model selection
    - Streaming
    - 95% coverage
    
47. **Issue #68:** Azure OpenAI provider
    - Azure-specific auth
    - Deployment configuration
    - API version handling
    - 95% coverage
    
48. **Issue #69:** AWS Bedrock provider
    - AWS auth
    - Model invocation
    - Streaming
    - 95% coverage
    
49. **Issue #70:** Provider switching UI (Web)
    - Dropdown selector
    - Model configuration
    - Real-time switching
    - 85% coverage
    
50. **Issue #71:** Provider switching in CLI
    - Model list command
    - Switch command
    - Configuration
    - 95% coverage

**Deliverables:**
- 4+ LLM providers supported
- Provider switching in both interfaces
- All providers tested with mocks

**Coverage Requirements:**
- Backend providers: 95%+
- UI components: 85%+

---

## Phase 6: Testing, Polish & Documentation (Week 6)

**GitHub Issues:** #81-100

### Tasks:
51. **Issue #81:** E2E test suite - Web
    - Complete user flows
    - Session management
    - Search functionality
    - Import/export
    
52. **Issue #82:** E2E test suite - CLI
    - Command execution
    - Interactive flows
    - Configuration
    
53. **Issue #83:** Cross-interface consistency tests
    - CLI vs GUI output comparison
    - Data consistency
    
54. **Issue #84:** Coverage gap analysis
    - Identify uncovered code
    - Write additional tests
    - Achieve coverage targets
    
55. **Issue #85:** Performance optimization
    - Query optimization
    - Lazy loading
    - Caching
    
56. **Issue #86:** Error handling audit
    - Consistent error messages
    - User-friendly errors
    - Error recovery
    
57. **Issue #87:** Setup scripts - User
    - Linux/macOS script
    - Windows batch file
    - Testing
    
58. **Issue #88:** Setup scripts - Developer
    - Dev dependencies
    - Pre-commit hooks
    - Testing
    
59. **Issue #89:** README.md completion
    - Feature documentation
    - Screenshots/GIFs
    - Usage examples
    - Troubleshooting
    
60. **Issue #90:** DEVELOPER.md completion
    - Architecture docs
    - API reference
    - Testing guide
    - Contributing guide
    
61. **Issue #91:** API documentation
    - Complete API.md
    - Endpoint examples
    - Request/response schemas
    
62. **Issue #92:** Search syntax documentation
    - SEARCH_SYNTAX.md
    - Query examples
    - Advanced features
    
63. **Issue #93:** Configuration documentation
    - CONFIGURATION.md
    - All settings explained
    - Examples
    
64. **Issue #94:** Docker setup (optional)
    - Dockerfile
    - docker-compose.yml
    - Documentation
    
65. **Issue #95:** CI/CD pipeline
    - GitHub Actions
    - Test automation
    - Coverage reporting
    - Build automation
    
66. **Issue #96:** Release preparation
    - Version tagging
    - Changelog
    - Release notes
    
67. **Issue #97:** Security audit
    - Dependency scanning
    - API key handling
    - Input validation
    
68. **Issue #98:** Accessibility audit
    - Web interface a11y
    - CLI screen reader support
    
69. **Issue #99:** Final testing pass
    - All platforms
    - All features
    - Edge cases
    
70. **Issue #100:** v0.1.0 Release
    - Tag release
    - Publish docs
    - Announcement

**Deliverables:**
- Complete test coverage
- All documentation finished
- Setup scripts working
- CI/CD operational
- v0.1.0 ready for release

**Coverage Requirements:**
- API: 100%
- Backend: 95%+
- CLI: 95%+
- Frontend: 85%+

---

## Coverage Enforcement

After each phase, verify coverage meets requirements:

```bash
# Backend coverage
cd backend
uv run pytest --cov=app --cov-report=html --cov-report=term
# Must show 95%+ for backend, 100% for api/routes/

# Frontend coverage
cd frontend
npm run test:coverage
# Must show 85%+

# CLI coverage
cd cli
npm run test:coverage
# Must show 95%+
```

If coverage drops below targets, create GitHub issues to address gaps before proceeding to next phase.

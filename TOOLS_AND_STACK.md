# TOOLS AND STACK
## Artificial Consciousness Architecture

**Version 1.0** | Date: 2025-11-30

---

## Overview

This document specifies all tools, libraries, frameworks, and technologies used in the project, organized by category and phase.

---

## Core Technologies

### Python Version
- **Python 3.11+**
  - Reason: Modern type hints, better performance, structural pattern matching
  - Features used: `match/case`, improved typing, async improvements

### Package Management
- **uv** or **poetry** (preference: uv for speed)
  - Dependency resolution
  - Virtual environment management
  - Lock file for reproducibility

---

## LLM Integration

### Primary LLM
- **Anthropic Claude API**
  - Model: `claude-sonnet-4-5-20250929` (Claude Sonnet 4.5)
  - Reason:
    - Strong reasoning capabilities
    - Long context window (200K tokens)
    - Less prone to sycophancy
    - Good at nuanced, philosophical responses
  - Usage:
    - Main response generation
    - Meta-cognitive reflections
    - Narrative construction

### API Client
- **anthropic** (official Python SDK)
  ```bash
  pip install anthropic
  ```

### Alternative/Supplementary Models

#### For Internal Processing (Optional)
- **Llama 3.2** (local, via Ollama)
  - Use case: Internal reflections, pattern detection
  - Reason: Free, fast, can run locally
  - Only if we want to reduce API costs for internal processing

#### For Embeddings
- **sentence-transformers** (HuggingFace)
  - Model: `all-MiniLM-L6-v2` or `all-mpnet-base-v2`
  - Use case: Semantic search in memories
  ```bash
  pip install sentence-transformers
  ```

---

## Data Storage

### Structured Data

#### Primary Database
- **PostgreSQL 15+** with **pgvector** extension
  - Use case: Structured data (memories, state snapshots, relationships)
  - Reason:
    - Robust, ACID compliant
    - pgvector for vector similarity search
    - JSON support for flexible schemas
  - Tables:
    - `episodic_memories`
    - `emotional_states`
    - `self_model_snapshots`
    - `reflections`
    - `dissonances`

#### Python Client
- **psycopg3** (PostgreSQL adapter)
  ```bash
  pip install psycopg[binary,pool]
  ```

#### ORM (Optional)
- **SQLAlchemy 2.0** (if we want ORM)
  - Async support
  - Type-safe queries
  ```bash
  pip install sqlalchemy[asyncio]
  ```

### Vector Database

#### For Semantic Memory Search
- **ChromaDB** (primary choice)
  - Use case: Semantic search over memories
  - Reason:
    - Easy to use
    - Embedded mode (no separate server)
    - Good Python integration
  - Alternative: **Qdrant** (if we need more scalability)

  ```bash
  pip install chromadb
  ```

### File-Based Storage

#### For Human-Readable Data
- **JSON files** (for auto-model, narratives, configurations)
  - Reason: Easy to inspect, version control friendly
  - Libraries:
    - Built-in `json` module
    - **orjson** (faster JSON serialization)
    ```bash
    pip install orjson
    ```

#### For Logs
- **JSONL** (JSON Lines)
  - Use case: Interaction logs, state evolution logs
  - Reason: Appendable, streamable, easy to parse

### Cache Layer
- **Redis**
  - Use case:
    - Recent state caching
    - Session management
    - Rate limiting
  - Python client: **redis-py**
  ```bash
  pip install redis
  ```

---

## Data Modeling & Validation

### Schema Definition
- **Pydantic 2.0**
  - Use case: All data models
  - Reason:
    - Type validation
    - Serialization/deserialization
    - Integration with FastAPI
  ```bash
  pip install pydantic
  ```

### Type Checking
- **mypy**
  - Static type checking
  - Reason: Catch type errors before runtime
  ```bash
  pip install mypy
  ```

---

## Web Framework (Optional API)

### REST API (if needed)
- **FastAPI**
  - Use case: HTTP API for interacting with the agent
  - Reason:
    - Fast
    - Auto-generated docs
    - Async support
    - Type hints integration
  ```bash
  pip install fastapi uvicorn
  ```

### WebSocket (for real-time interaction)
- **FastAPI WebSocket** support
  - Use case: Real-time bidirectional communication

---

## Logging & Observability

### Logging
- **structlog**
  - Use case: Structured logging with context
  - Reason:
    - JSON output
    - Context binding
    - Better than stdlib logging
  ```bash
  pip install structlog
  ```

### Log Storage
- **File-based** (JSONL files)
  - Levels:
    - `data/logs/system/` - System logs
    - `data/logs/interactions/` - User interactions
    - `data/logs/decisions/` - Decision logs
    - `data/logs/reflections/` - Reflection logs

### Metrics (Optional)
- **Prometheus** + **Grafana** (if we want dashboards)
  - Use case: Visualize system metrics over time
  - Metrics to track:
    - Emotional state dimensions
    - Memory consolidation rate
    - Dissonance frequency
    - Attention competition results

---

## Testing

### Unit Testing
- **pytest**
  - De facto standard for Python testing
  - Plugins:
    - `pytest-asyncio` - async test support
    - `pytest-cov` - coverage reports
    - `pytest-mock` - mocking utilities
  ```bash
  pip install pytest pytest-asyncio pytest-cov pytest-mock
  ```

### Property-Based Testing
- **hypothesis**
  - Use case: Generate test cases automatically
  - Reason: Find edge cases in state transitions, memory consolidation
  ```bash
  pip install hypothesis
  ```

### Coverage
- **coverage.py** (via pytest-cov)
  - Target: >80% coverage for core modules

---

## Code Quality

### Linting
- **ruff**
  - Modern, fast linter
  - Replaces: flake8, isort, pyupgrade
  ```bash
  pip install ruff
  ```

### Formatting
- **black**
  - Opinionated code formatter
  - Reason: Consistent style, no debates
  ```bash
  pip install black
  ```

### Pre-commit Hooks
- **pre-commit**
  - Run linters/formatters before commits
  ```bash
  pip install pre-commit
  ```

  `.pre-commit-config.yaml`:
  ```yaml
  repos:
    - repo: https://github.com/psf/black
      rev: 23.11.0
      hooks:
        - id: black
    - repo: https://github.com/astral-sh/ruff-pre-commit
      rev: v0.1.6
      hooks:
        - id: ruff
    - repo: https://github.com/pre-commit/mirrors-mypy
      rev: v1.7.1
      hooks:
        - id: mypy
  ```

---

## Development Tools

### Interactive Development
- **IPython** / **Jupyter**
  - Use case: Interactive exploration, analysis
  - Notebooks for:
    - Memory pattern analysis
    - Emotional state visualization
    - Identity evolution tracking
  ```bash
  pip install ipython jupyter
  ```

### Debugging
- **ipdb** (IPython debugger)
  ```bash
  pip install ipdb
  ```

### Environment Management
- **.env** files
  - Library: **python-dotenv**
  ```bash
  pip install python-dotenv
  ```

---

## Visualization & Analysis

### Data Visualization
- **matplotlib** + **seaborn**
  - Use case: Emotional state evolution, memory patterns
  ```bash
  pip install matplotlib seaborn
  ```

### Interactive Plots
- **plotly**
  - Use case: Interactive dashboards
  ```bash
  pip install plotly
  ```

### Network Graphs (for memory connections)
- **networkx** + **pygraphviz**
  - Use case: Visualize memory relationship graphs
  ```bash
  pip install networkx
  ```

---

## Utilities

### Date/Time
- **pendulum** or **arrow**
  - Better than stdlib `datetime`
  - Reason: Timezone handling, human-readable deltas
  ```bash
  pip install pendulum
  ```

### UUID Generation
- **uuid** (stdlib)
  - Use case: Memory IDs, snapshot IDs

### Hashing
- **hashlib** (stdlib)
  - Use case: Content hashing, deduplication

---

## Async & Concurrency

### Async Framework
- **asyncio** (stdlib)
  - Use case: Async LLM calls, DB operations

### HTTP Client (async)
- **httpx**
  - Use case: Async HTTP requests
  ```bash
  pip install httpx
  ```

### Task Queue (Optional, for later phases)
- **Celery** + **Redis**
  - Use case: Background reflection loops, scheduled tasks
  ```bash
  pip install celery[redis]
  ```

---

## Configuration Management

### Configuration
- **pydantic-settings**
  - Type-safe configuration from env vars
  ```bash
  pip install pydantic-settings
  ```

### Example:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    llm_model: str = "claude-sonnet-4-5-20250929"
    llm_max_tokens: int = 4096
    llm_temperature: float = 0.7

    database_url: str
    redis_url: str

    log_level: str = "INFO"

    class Config:
        env_file = ".env"
```

---

## Containerization (Optional)

### Docker
- **Docker** + **Docker Compose**
  - Use case: Consistent dev environment, deployment
  - Services:
    - App container (Python)
    - PostgreSQL
    - Redis
    - (Optional) Grafana/Prometheus

### `docker-compose.yml` example:
```yaml
version: '3.8'

services:
  app:
    build: .
    volumes:
      - ./src:/app/src
      - ./data:/app/data
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/consciousness
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: consciousness
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

---

## Documentation

### Documentation Generation
- **mkdocs** + **mkdocs-material**
  - Use case: Generate beautiful docs from markdown
  ```bash
  pip install mkdocs mkdocs-material
  ```

### API Documentation
- **FastAPI** auto-generates OpenAPI docs (if we use REST API)

### Docstrings
- **Google-style** or **NumPy-style** docstrings
- Type hints in all functions

---

## Version Control

### Git
- **Git** (obviously)
- **GitHub** (or GitLab)

### Commit Conventions
- **Conventional Commits**
  - Format: `<type>(<scope>): <description>`
  - Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

### Branching Strategy
- **Main branch**: `main` (stable)
- **Development branch**: `develop`
- **Feature branches**: `feature/<name>`
- **Phase branches**: `phase/<number>`

---

## CI/CD (Optional, for later)

### GitHub Actions
- Run tests on PR
- Lint/format check
- Type check
- Coverage report

### `.github/workflows/test.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest --cov=src tests/
      - name: Type check
        run: mypy src/
      - name: Lint
        run: ruff check src/
```

---

## Complete Dependency List

### `requirements.txt` (Production)
```txt
# LLM
anthropic>=0.39.0

# Data & Storage
psycopg[binary,pool]>=3.1.0
chromadb>=0.4.0
redis>=5.0.0
orjson>=3.9.0

# Embeddings
sentence-transformers>=2.2.0

# Data Modeling
pydantic>=2.5.0
pydantic-settings>=2.1.0

# Utils
structlog>=23.2.0
pendulum>=3.0.0
python-dotenv>=1.0.0

# Web (optional)
fastapi>=0.109.0
uvicorn[standard]>=0.25.0

# Async
httpx>=0.26.0
```

### `requirements-dev.txt` (Development)
```txt
# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
pytest-mock>=3.12.0
hypothesis>=6.92.0

# Code Quality
black>=23.12.0
ruff>=0.1.6
mypy>=1.7.1
pre-commit>=3.6.0

# Development
ipython>=8.18.0
ipdb>=0.13.0

# Visualization
matplotlib>=3.8.0
seaborn>=0.13.0
plotly>=5.18.0
networkx>=3.2.0

# Documentation
mkdocs>=1.5.0
mkdocs-material>=9.5.0

# Notebooks
jupyter>=1.0.0
```

---

## Performance Benchmarks (Expected)

### Phase 0
- **Response time**: < 2 seconds
- **Memory operations**: < 100ms
- **State updates**: < 50ms

### Phase 3+ (Full System)
- **Response time**: < 5 seconds
- **Workspace processing**: < 500ms
- **Reflection loop**: < 10 seconds (async, doesn't block)

### Resource Usage
- **Memory**: < 2GB RAM
- **Storage**: ~500MB per month (with pruning)
- **API costs**: ~$20-50/month (depends on usage)

---

## Security Considerations

### API Keys
- **Never commit API keys**
- Use `.env` files (gitignored)
- Rotate keys periodically

### Data Privacy
- **No PII storage**
- Anonymize user identifiers
- Clear data retention policy

### Dependencies
- Regular security updates
- Use **dependabot** or **renovate** for automated updates

---

## Monitoring & Alerting (Future)

### Error Tracking
- **Sentry** (optional)
  - Use case: Production error tracking

### Uptime Monitoring
- **UptimeRobot** or similar (if we deploy)

---

## Deployment (Future Consideration)

### Hosting Options
- **Cloud**: AWS, GCP, or Azure
- **VPS**: DigitalOcean, Linode
- **Local**: Development machine

### Deployment Tools
- **Docker** + **docker-compose**
- **Kubernetes** (overkill for this project)

---

## Phase-Specific Tools

### Phase 0
- Core: Python, Claude API, PostgreSQL, ChromaDB
- Minimal dependencies

### Phase 1+
- Add: More sophisticated state management
- Same stack

### Phase 3+
- Potentially add: Task queue (Celery) for async reflections
- Visualization tools for workspace dynamics

---

## Tool Selection Philosophy

1. **Simplicity over complexity**: Choose simple tools that work
2. **Standard over exotic**: Prefer widely-used, well-documented tools
3. **Performance matters, but not prematurely**: Optimize when needed
4. **Local-first when possible**: Minimize external dependencies
5. **Type safety**: Strong preference for typed libraries

---

## Getting Started Checklist

- [ ] Install Python 3.11+
- [ ] Install PostgreSQL 15+ with pgvector
- [ ] Install Redis (optional for Phase 0)
- [ ] Clone repository
- [ ] Create virtual environment
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Install dev dependencies: `pip install -r requirements-dev.txt`
- [ ] Copy `.env.example` to `.env`
- [ ] Add Anthropic API key to `.env`
- [ ] Initialize database: `python scripts/setup_database.py`
- [ ] Run tests: `pytest`
- [ ] Start development!

---

**Next Steps**:
1. Set up development environment
2. Initialize project structure
3. Configure tools (linters, formatters, pre-commit)
4. Write first tests
5. Begin Phase 0 implementation

# iOS Test Automator - Technology Profile

**Version**: 1.0.0
**Last Updated**: 2026-02-07
**Purpose**: Document technology-specific choices that may evolve over time

This document captures current technology decisions. Unlike the Constitution, these choices
can change without requiring formal amendments. The Constitution defines contracts and
non-negotiables; this document defines "what we're using right now."

---

## Backend Stack

### API Framework
- **Choice**: FastAPI 0.109+ (required by Constitution Principle II)
- **Rationale**: Async support, automatic validation, OpenAPI docs
- **Migration Path**: N/A (constitutional requirement)

### LLM Orchestration
- **Choice**: LangChain 0.1.0+ with LangGraph 0.0.40+
- **Interface**: `LLMClient` abstract base class (constitutional requirement)
- **Rationale**: State machines for compile/repair loops, proven patterns
- **Migration Path**: Implement new LLMClient subclass, run parity tests, switch via config

### LLM Provider
- **Choice**: Anthropic Claude (claude-3-5-sonnet-20240620 or newer)
- **API**: Anthropic SDK via LangChain
- **Rationale**: Best performance for code generation, long context windows
- **Migration Path**: Add new provider behind LLMClient interface

### Python Version
- **Choice**: Python 3.11
- **Rationale**: asyncio improvements, better error messages
- **Migration Path**: Update `.python-version`, test compatibility, update CI

---

## RAG System

### Vector Store
- **Choice**: ChromaDB 0.4.22+
- **Storage**: Local SQLite-backed (`rag_store/` directory)
- **Rationale**: Local-first, embeddable, no external dependencies, persistent storage
- **Migration Path**: Export vectors, import to new store, verify retrieval parity

### Embedding Model
- **Choice**: `sentence-transformers/all-mpnet-base-v2`
- **Dimension**: 768
- **Rationale**: Good balance of quality and speed, works offline
- **Migration Path**: Re-embed corpus with new model, compare retrieval quality

### Swift Code Parser
- **Choice**: Tree-sitter with swift grammar (tree-sitter-swift)
- **Rationale**: Accurate syntax parsing, extracts symbols and metadata
- **Migration Path**: Abstract parser interface, compare extraction quality

### Metadata Schema
```python
{
  "code_chunk": str,           # The actual Swift code
  "file_path": str,            # Relative path from ios-app/
  "symbol_name": str,          # Class, function, or property name
  "symbol_type": str,          # "class", "function", "property", "struct", "enum"
  "access_level": str,         # "public", "internal", "private"
  "ui_type": Optional[str],    # "SwiftUI", "UIKit", None
  "dependencies": List[str]    # Imported modules and referenced types
}
```

---

## Frontend

### UI Framework
- **Choice**: Streamlit 1.30+
- **Rationale**: Rapid prototyping, Python-native, no React/JS needed
- **Migration Path**: Build REST client first, then migrate UI to new framework

### Styling
- **Choice**: Streamlit built-in themes only (no custom CSS)
- **Rationale**: Simplicity, maintainability
- **Migration Path**: N/A unless migrating away from Streamlit

### State Management
- **Choice**: Streamlit `st.session_state`
- **Rationale**: Built-in, simple, sufficient for MVP
- **Migration Path**: Migrate to Redux/Zustand if complexity grows

---

## iOS Tooling

### Xcode Version
- **Choice**: Xcode 15.2 (Swift 5.9.2)
- **Location**: Documented in `.xcode-version` file and README
- **Rationale**: Latest stable with good SwiftUI support
- **Migration Path**: Update `.xcode-version`, test generated code, update docs

### Build System
- **Choice**: xcodebuild (native Xcode CLI)
- **Rationale**: Official tool, no third-party dependencies
- **Migration Path**: Consider fastlane or xcodegen if build complexity grows

### Simulator Control
- **Choice**: simctl (native iOS Simulator CLI)
- **Alternative Considered**: idb (Facebook's iOS Device Bridge)
- **Rationale**: simctl is native, no installation required, sufficient for MVP
- **Migration Path**: Add idb support behind IOSController interface

### Video Recording
- **Choice**: simctl io recordVideo
- **Format**: MP4 (H.264)
- **Rationale**: Native support, no external tools
- **Migration Path**: Consider custom screen recorder for higher quality

---

## Observability

### Error Tracking
- **Choice**: Sentry 1.40+ (Python SDK)
- **Rationale**: Production-grade, excellent Python support, free tier
- **Migration Path**: Abstract error tracker interface, add new provider

### Distributed Tracing
- **Choice**: OpenTelemetry + Sentry tracing
- **Rationale**: Industry standard, integrates with Sentry
- **Migration Path**: Swap OTEL exporter (Jaeger, Zipkin, etc.)

### Logging
- **Choice**: Python `logging` module with JSON formatter
- **Rationale**: Standard library, structured logs for parsing
- **Migration Path**: Switch to structlog or loguru if more features needed

---

## Data Storage

### Run History Database
- **Choice**: SQLite 3.40+
- **Location**: `.specify/memory/run_history.db`
- **Rationale**: Local, embedded, no external database server
- **Migration Path**: Export to CSV, import to Postgres/MySQL if team collaboration needed

### Artifact Storage
- **Choice**: Local filesystem (`artifacts/<timestamp>/`)
- **Organization**: Subdirectories for code, logs, videos, traces
- **Rationale**: Simple, fast, no cloud dependencies
- **Migration Path**: Add S3/GCS backend, keep local as cache

---

## Development Tools

### Code Formatter
- **Choice**: black 24.0+ (line length 100)
- **Rationale**: Opinionated, no configuration debates
- **Migration Path**: N/A (industry standard)

### Linter
- **Choice**: pylint 3.0+
- **Alternative Considered**: ruff (much faster)
- **Rationale**: Comprehensive, well-established
- **Migration Path**: Switch to ruff if speed becomes issue

### Type Checker
- **Choice**: mypy 1.8+ (strict mode)
- **Rationale**: Best Python type checker, IDE integration
- **Migration Path**: Consider pyright if performance issues

### Import Sorter
- **Choice**: isort 5.13+ (black-compatible profile)
- **Rationale**: Integrates with black, consistent imports
- **Migration Path**: N/A (rarely changes)

### Testing Framework
- **Choice**: pytest 7.4+
- **Async Support**: pytest-asyncio 0.23+
- **Rationale**: Industry standard, excellent async support
- **Migration Path**: N/A (industry standard)

---

## Deployment (Future)

### Containerization
- **Choice**: TBD (Docker likely)
- **Rationale**: Not needed for MVP (local development only)
- **Migration Path**: Add Dockerfile when needed for production

### CI/CD
- **Choice**: TBD (GitHub Actions likely)
- **Rationale**: Not needed for MVP (manual testing)
- **Migration Path**: Add workflow files when team grows

---

## Decision Log

### 2026-02-07: Initial Tech Profile
- Selected ChromaDB over Pinecone (local-first principle)
- Selected Streamlit over React (rapid prototyping, Python-native)
- Selected simctl over idb (native tool, no installation)
- Selected SQLite over Postgres (local database, embedded)
- Selected sentence-transformers over OpenAI embeddings (offline support)

---

## Evaluation Criteria for Technology Changes

When considering technology swaps, evaluate:

1. **Constitutional Compliance**: Does it violate any principles? (FastAPI, LLMClient interface, etc.)
2. **Migration Cost**: How many lines of code change? How long to migrate?
3. **Performance**: Measurable improvement? Benchmarks required.
4. **Simplicity**: Does it reduce or increase complexity? (Principle V)
5. **Team Knowledge**: Do we know this tech? Learning curve?
6. **Dependencies**: Does it add external dependencies? Security implications?

**Threshold for Change**: New technology must be 2-3x better on key metric (speed, accuracy, cost)
to justify migration cost. Marginal improvements (10-20%) are not worth switching.

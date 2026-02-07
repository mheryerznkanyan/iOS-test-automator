<!--
Sync Impact Report:
- Version change: INITIAL → 1.0.0
- New constitution created from template
- Added 6 core principles:
  1. AI-First Development (LLMClient interface with LangChain default)
  2. FastAPI for APIs
  3. Resource Caching via FastAPI DI (not singleton pattern)
  4. Pydantic Input/Output Contract (run() method pattern)
  5. Simplicity Over Complexity
  6. Developer Experience
- Moved technology-specific choices to Tech Profile document
- Added concrete security constraints for code execution
- Added IOSController abstraction requirement
- Templates requiring updates:
  ✅ .specify/templates/spec-template.md - validated
  ✅ .specify/templates/plan-template.md - validated
  ✅ .specify/templates/tasks-template.md - validated
  ✅ .specify/templates/checklist-template.md - validated
  ⚠ Tech Profile document needs creation (.specify/memory/tech-profile.md)
- Follow-up TODOs: Create tech-profile.md with Streamlit/Chroma/embeddings choices
-->

# iOS Test Automator Constitution

## Core Principles

### I. AI-First Development

**All LLM usage MUST go through LLMClient interface; LangChain + LangGraph is the default implementation.**

- LLM orchestration via `LLMClient` interface (abstract base class)
- Default implementation: LangChain + LangGraph with compile/repair loops
- Direct SDK calls allowed only behind `LLMClient` with parity tests
- Implement compile/repair loops: generate test code → compile → fix errors → retry
- Maintain prompts as first-class artifacts (version controlled, documented, tested)
- LangGraph state machines for multi-step test generation and validation workflows
- Capture all LLM interactions (prompts, responses, tokens) for debugging and improvement

**Compile/Repair Loop Requirements**:
```
1. Generate test code with LLM
2. Compile Swift code via IOSController (see Principle V)
3. If errors: Extract compiler errors → Send to LLM → Regenerate
4. Retry up to 3 times with exponential backoff
5. Return final code or compilation errors with full trace
```

**Rationale**: The `LLMClient` interface allows swapping implementations (OpenAI, Claude, local models)
without changing business logic. LangChain provides proven patterns but isn't forced when direct
SDK calls are more appropriate. Compile/repair loops improve code quality automatically.

### II. FastAPI for APIs

**All API development MUST use FastAPI framework.**

- RESTful API endpoints using FastAPI routing and dependency injection
- Pydantic models for request/response validation (type safety enforced)
- Async/await patterns for I/O-bound operations (database, LLM calls, file I/O)
- OpenAPI documentation auto-generated and always accessible at `/docs`
- No Flask, Django REST, or custom HTTP servers permitted
- FastAPI middleware for logging, error handling, CORS, and Sentry integration
- Dependency injection used for all shared resources (see Principle III)

**Rationale**: FastAPI provides modern async support, automatic validation, excellent
performance, and built-in OpenAPI docs that align with rapid development needs.

### III. Resource Caching via FastAPI DI

**Shared expensive resources MUST be cached once per process and provided via FastAPI DI.**

- Configuration managers, LLM clients, database connections, RAG systems use cached resources
- Allowable implementations:
  1. **Module-level cached instance**: `_instance = None` with lazy init
  2. **@lru_cache factory**: `@lru_cache(maxsize=1)` decorator on factory function
  3. **App lifespan initialization**: FastAPI `@asynccontextmanager` for `app.router.lifespan`
- For async initialization: Provide explicit `await get_instance()` or `await init()` function
- Resources MUST be testable: Support dependency override (`app.dependency_overrides`)
- Do NOT use async metaclass singleton pattern (`async def __call__` doesn't work)
- Stateless services should be per-request (not cached)

**Example Pattern (Module-level cache with async init)**:
```python
_rag_client: Optional[RAGClient] = None

async def get_rag_client() -> RAGClient:
    global _rag_client
    if _rag_client is None:
        _rag_client = RAGClient()
        await _rag_client.init()
    return _rag_client

# FastAPI usage
@app.get("/search")
async def search(rag: RAGClient = Depends(get_rag_client)):
    return await rag.search(...)
```

**Rationale**: FastAPI's dependency injection system is designed for this use case.
Module-level caching and `@lru_cache` work reliably. App lifespan ensures proper cleanup.
Avoid complex metaclass patterns that create confusing runtime behavior.

### IV. Pydantic Input/Output Contract

**All service classes MUST have a run() method that takes Pydantic input and returns Pydantic output.**

- Every service/agent class MUST implement a `run()` method as the primary interface
- The `run()` method signature: `async def run(self, input: PydanticModel) -> PydanticModel`
- Input and output MUST be Pydantic models (enables automatic validation and serialization)
- Class-specific helper functions MUST be instance methods inside the class (no free functions)
- Private helpers should be prefixed with underscore: `_helper_method()`
- Public methods beyond `run()` are allowed only if they serve a clear, distinct purpose

**Example**:
```python
class TestGenerator:
    async def run(self, input: TestGenerationRequest) -> TestGenerationResponse:
        context = await self._fetch_rag_context(input.app_path)
        code = await self._generate_with_llm(input.description, context)
        validated = await self._compile_and_repair(code)
        return TestGenerationResponse(test_code=validated, metadata={...})

    async def _fetch_rag_context(self, app_path: str) -> str:
        # Private helper method inside class
        ...
```

**Rationale**: Standardizing on Pydantic ensures type safety, automatic validation,
and seamless FastAPI integration. The `run()` pattern provides a clear, consistent
interface across all service classes. Keeping helpers inside classes improves cohesion.

### V. Simplicity Over Complexity

**Choose the straightforward solution unless complexity is justified.**

- Prefer straightforward implementations over clever abstractions
- Avoid premature optimization and over-engineering
- Keep the API surface minimal (fewer endpoints with clear purposes)
- No feature should require more than 3 steps for users to complete
- Documentation should be clear, concise, and example-driven
- Code should be readable without extensive comments

**Rationale**: This is a research/development tool. Maintainability and quick iteration
matter more than perfect architecture. Simple code is debuggable code.

### VI. Developer Experience First

**Optimize for fast feedback loops and clear error messages.**

- Test generation and execution MUST provide real-time status updates
- Error messages MUST be actionable (what went wrong, how to fix it)
- Setup process MUST complete in under 10 minutes with clear instructions
- Interactive UI for all operations (no CLI-only workflows for core features)
- Video recordings of test runs available immediately after execution
- Configuration errors detected at startup, not during operation
- Run history maintained for all test generation and execution attempts (see Run History schema)

**Rationale**: Developers using this tool need quick validation cycles. Frustrating UX
leads to abandonment. Clear feedback accelerates debugging and builds trust.

## Technical Standards

### Security & Code Execution Safety

**Generated Swift code MUST follow concrete security constraints:**

1. **File System Isolation**
   - Generated files ONLY under `ios-app/SampleAppUITests/` directory
   - No writes outside this fixed directory (enforce in IOSController)
   - Test artifacts stored under `artifacts/<timestamp>/` (read-only for generated code)

2. **Shell Command Safety**
   - NEVER interpolate user input into shell command strings
   - Use argument arrays for subprocess calls: `["xcodebuild", "test", "-scheme", scheme]`
   - Allowlist for `xcodebuild` arguments: `-scheme`, `-destination`, `-resultBundlePath`
   - Allowlist for `simctl` arguments: `boot`, `shutdown`, `install`, `launch`, `io`, `privacy`
   - Reject any shell metacharacters in user-provided paths or test descriptions

3. **Logging & Redaction**
   - Store all subprocess output (stdout/stderr) in artifact directory
   - Redact API keys, environment variables, absolute paths from user-facing logs
   - Sentry breadcrumbs MUST NOT contain user source code or secrets
   - Log file retention: 30 days local, then archive or delete

4. **Input Validation**
   - Test descriptions: Max 2000 characters, no shell metacharacters
   - File paths: Must be relative, no `..`, must exist within project
   - Simulator IDs: UUID format only (validate with regex)
   - Generated Swift code: Syntax validation before write (xcodebuild -dry-run or swiftc -parse)

**Rationale**: Concrete constraints are enforceable and testable. Vague "sanitize input"
rules are not. These constraints prevent shell injection, filesystem escape, and log leaks.

### iOS Control Plane

**All iOS simulator and build operations MUST go through IOSController abstraction.**

- Single `IOSController` class for all device/simulator operations
- Tool interface for agent + API (no scattered subprocess calls)
- MVP: simctl + xcodebuild only (idb support deferred)
- Operations: boot simulator, install app, run tests, capture video, compile code
- Subprocess management: Timeout enforcement, stdout/stderr capture, signal handling
- Error handling: Parse xcodebuild/simctl errors into structured exceptions

**Example**:
```python
class IOSController:
    async def compile_test(self, test_file: Path) -> CompileResult:
        # Uses allowlisted xcodebuild args only
        ...

    async def run_test(self, test_name: str, simulator_id: str, record_video: bool) -> TestRunResult:
        # Uses allowlisted simctl args only
        ...
```

**Rationale**: Centralized control plane prevents security issues (scattered subprocess calls)
and improves testability (mock IOSController). Explicit tool choice (simctl+xcodebuild vs idb)
avoids confusion and ensures consistent behavior.

### Swift Version

**Swift version is pinned to the Xcode version used in this repository; Swift version inherited from Xcode.**

- Xcode version specified in `.xcode-version` file or documented in README
- Generated test code must compile with this Xcode version
- No attempts to support multiple Swift versions simultaneously
- Update Xcode version explicitly when upgrading (document in changelog)

**Rationale**: Swift language features change with Xcode releases. Pinning Xcode avoids
compatibility issues. Trying to support multiple Swift versions is complexity without benefit.

### Reliability & Observability

**Sentry Integration (Error Tracking)**
- All backend errors MUST be captured in Sentry (exceptions, validation failures)
- Performance monitoring for API endpoints (slow queries, LLM timeouts)
- User context attached to errors (request ID, test description length, timestamp)
- Environment-specific Sentry projects (dev/staging/production)
- Breadcrumbs for debugging multi-step workflows (RAG query → LLM call → compile)
- NEVER log API keys, source code, or absolute paths to Sentry

**Artifact Capture**
- All generated test code saved with metadata (timestamp, prompt, LLM model, trace_id)
- Compiler errors and repair attempts logged for each generation
- Video recordings of test execution archived with test metadata
- LLM prompts and responses captured for prompt engineering analysis
- Storage: `artifacts/<timestamp>/` with subdirs for code, logs, videos, traces
- Retention: 30 days, then archive to S3 or delete

**Tracing**
- Distributed tracing for request flows (API → RAG → LLM → Compiler → Simulator)
- Trace IDs propagated across service boundaries (in headers, logs, artifacts)
- Span timing for performance analysis (identify bottlenecks)
- Trace sampling: 100% for errors, 10% for success (configurable)

**Run History (SQLite)**
- Database schema (minimal):
  ```sql
  CREATE TABLE runs (
    run_id TEXT PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    status TEXT NOT NULL,  -- 'success', 'compile_error', 'execution_error', 'llm_error'
    test_description TEXT NOT NULL,
    steps TEXT NOT NULL,   -- JSON array of step names
    durations TEXT NOT NULL,  -- JSON object of step durations (ms)
    artifacts_path TEXT NOT NULL,  -- Relative path to artifacts/
    error_code TEXT,  -- Error classification (e.g., 'COMPILE_ERROR', 'TIMEOUT')
    metadata TEXT  -- JSON for extensibility
  );
  ```
- SQLite database location: `.specify/memory/run_history.db`
- Accessible via UI (filterable by date, status, test name)
- Export as CSV/JSON for analysis
- No PII or sensitive data in run history

**Rationale**: Sentry provides production-grade error tracking. Artifacts enable debugging
without reproduction. Tracing identifies performance bottlenecks. SQLite is simple, local,
and sufficient for MVP run history. Concrete schema prevents scope creep.

## Development Rules

### Code Review

- Self-review required before every commit (re-read diffs, test locally)
- Generated test code MUST be executed on simulator before merging
- Prompt changes MUST be validated with multiple test scenarios (edge cases)
- Security review: Verify no shell interpolation, file path escapes, or log leaks
- Performance check: No endpoint regressions (test generation time should not increase)
- Verify Sentry integration captures errors correctly (test error paths)

### Testing Requirements

- All API endpoints MUST have example requests documented in README
- Generated Swift tests MUST be validated for syntax (xcodebuild -dry-run or swiftc -parse)
- Manual verification of test execution required (watch video recording)
- Maintain test scenario library (`test_scenarios.json`) with diverse examples
- RAG system MUST be tested with different codebases (not just SampleApp)
- Pydantic models MUST be tested with invalid inputs (validation edge cases)
- Compile/repair loops MUST be tested with intentionally broken code
- IOSController MUST be tested with mocked subprocess calls (no actual simulator required)
- Sentry integration tested with mock errors (verify capture and context)

### Commit Conventions

**Use conventional commits format:**

`<type>(<scope>): <description>`

**Types**: `feat` | `fix` | `docs` | `refactor` | `test` | `chore`

**Scopes**: `backend` | `ui` | `rag` | `docs` | `prompts` | `models` | `sentry` | `artifacts` | `ios-controller`

**Examples**:
- `feat(backend): add batch test generation endpoint`
- `fix(rag): improve context retrieval with metadata filters`
- `feat(ios-controller): add compile-only mode for syntax validation`
- `refactor(prompts): add compile/repair loop to test generation`
- `feat(sentry): add distributed tracing for LLM calls`
- `fix(artifacts): redact absolute paths from captured logs`

### Code Style

**Python Classes**
- All service/agent classes MUST implement `async def run(input: Model) -> Model`
- Class-specific helpers MUST be instance methods (prefix private with `_`)
- Expensive resources accessed via FastAPI DI (see Principle III)
- Type hints required for all methods (input/output types explicit)
- LangGraph workflows use state machine pattern with typed state

**Python General**
- Formatter: `black` (line length 100 characters)
- Linter: `pylint` (enforce code quality rules)
- Type Hints: Required for all public functions and class methods
- Imports: Sorted with `isort` (standard lib → third party → local)
- Docstrings: Google style (Args, Returns, Raises sections)
- Concurrency: Use `asyncio` library exclusively (no threading module)
- Error handling: All exceptions captured in Sentry with context

**Swift**
- Follow Swift API Design Guidelines (Apple's official conventions)
- Generated test code MUST match Apple's XCTest naming conventions
- Clear test naming: `test_featureName_scenario_expectedResult`
- Example: `test_loginButton_whenTapped_displaysHomeScreen`

**Naming Conventions**
- Python: `snake_case` for functions/variables, `PascalCase` for classes
- Swift: `camelCase` for functions/variables, `PascalCase` for classes/protocols
- Files: `lowercase-with-hyphens` for configs, `snake_case.py` for Python modules
- Endpoints: `/kebab-case` for REST API paths (e.g., `/generate-test-with-rag`)
- Environment Variables: `SCREAMING_SNAKE_CASE` (e.g., `ANTHROPIC_API_KEY`, `SENTRY_DSN`)
- Pydantic Models: `PascalCase` with descriptive suffixes (`TestGenerationRequest`, `TestGenerationResponse`)
- Artifacts: `artifacts/<timestamp>/<artifact_type>/<filename>`

### Quality Standards

**Generated Swift Code Quality**
- MUST compile without errors after compile/repair loop (max 3 iterations)
- Follow iOS testing best practices (accessibility identifiers, wait conditions)
- Include appropriate wait conditions (`waitForExistence`, timeouts)
- Handle edge cases: app not launched, elements not found, simulator issues
- Clear assertion messages (XCTAssertTrue with descriptive failure messages)

**Pydantic Model Quality**
- Models MUST have descriptive field names and types
- Use Field() for validation constraints (min/max length, regex patterns)
- Include docstrings for complex models
- Example values in Config.schema_extra for documentation
- Nested models preferred over deeply nested dicts

**Documentation**
- README.md in each major directory (backend, ui, rag, ios-app, artifacts)
- API endpoints documented with curl examples and expected responses
- Environment variables documented in `.env.example` with explanations
- Architecture decisions recorded in ADRs when significant choices made
- Prompt templates documented with input/output examples
- Pydantic models documented with example JSON payloads
- Sentry configuration documented (DSN setup, environment config)
- Artifact storage structure documented (directory layout, retention policy)

**Error Handling**
- Graceful degradation when LLM unavailable (offline mode, cached responses)
- Clear error messages for missing configuration (which .env variable missing)
- Validation errors return actionable feedback (not just "Invalid input")
- Log errors with context for debugging (request ID, timestamp, stack trace)
- User-facing errors hide sensitive info (API keys, internal paths)
- Pydantic validation errors MUST be caught and reformatted for users
- All backend errors captured in Sentry with user context (no PII)

## Governance

### Amendment Process

- Constitution amendments require explicit documentation of changes (this report format)
- Breaking changes (MAJOR version) require migration plan for existing features
- Non-breaking additions (MINOR version) require validation of template consistency
- All amendments must update dependent templates (spec, plan, tasks, checklists)

### Compliance Review

- All PRs and code reviews MUST verify compliance with constitution principles
- Principle violations require explicit justification or constitution amendment
- NON-NEGOTIABLE principles (require MAJOR version change to amend):
  - LLMClient interface for all LLM usage (Principle I)
  - FastAPI for APIs (Principle II)
  - Resource caching via FastAPI DI (Principle III)
  - Pydantic input/output contract with `run()` method (Principle IV)
  - IOSController abstraction for all iOS operations
- Asyncio MUST be used for concurrency (no threading module)
- Complexity MUST be justified (Principle V applies: default is simplicity)
- Security violations (shell interpolation, path escapes, log leaks) block merges immediately
- Sentry integration required for all production deployments

### Technology Choices

Technology-specific choices (Streamlit, ChromaDB, sentence-transformers, etc.) are documented
in `.specify/memory/tech-profile.md`. These choices are expected to evolve and do not require
constitution amendments. The constitution focuses on contracts, non-negotiables, and security/
observability requirements that remain stable across technology changes.

### Current Limitations (Future Work)

These are acknowledged limitations to be addressed in future iterations:
- iOS Simulator only (no real device support yet)
- Single app project support (only SampleApp configured)
- simctl + xcodebuild only (idb support deferred)
- Manual RAG index updates (no automatic re-indexing on code changes)
- No CI/CD pipeline (manual testing and deployment)
- Run history stored locally (no cloud sync or team collaboration)
- Artifact retention: manual cleanup after 30 days

**Version**: 1.0.0 | **Ratified**: 2026-02-07 | **Last Amended**: 2026-02-07

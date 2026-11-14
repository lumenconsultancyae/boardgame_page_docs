# ADR 0001: Layered Service Architecture, Interactive SVG/Mermaid Rule Diagrams, and SQLite Persistence

## Context

Boardgame Hub requires a fast, reliable web application capable of tracking board game collections and play sessions, generating visual rule flowcharts and analytics graphs, formatting WhatsApp share messages (`wa.me`), and managing UAE boardgame community events. Both in-process unit/integration tests and containerized browser BDD E2E suites must run deterministically with zero external network dependencies.

## Decision Drivers

- Strict inward dependency rule (`domain` $\leftarrow$ `application` $\leftarrow$ `infrastructure` / `api`).
- Instantaneous startup and deterministic test execution in both local Python environments and Docker containers.
- XSS-safe interactive flowchart rendering (`svg` DOM construction + exportable Mermaid v11 `flowchart LR` definitions).
- One-click WhatsApp sharing compatibility across desktop and mobile browsers via `https://wa.me/?text=...` deep links.

## Considered Options

1. **Option A (Selected)**: Layered Python 3.11+ service with SQLite persistence (`SqliteBoardgameRepository`), pure stateless diagram/analytics/WhatsApp builders (`src/utils/formatting.py`), and a zero-build vanilla ES6 + SVG frontend.
2. **Option B**: External PostgreSQL + heavy external JS bundler stack.
3. **Option C**: Static Markdown site without interactive session logging or dynamic UAE event RSVPs.

## Decision Outcome

Chosen option: **Option A**, because it enforces clean architectural boundaries (`BoardgameRepositoryPort`), achieves 98% branch coverage in `< 1s`, renders interactive SVG flowcharts and Mermaid v11 code natively without XSS sinks, and persists collection, session, and UAE event updates reliably in SQLite.

## Consequences

- **Positive**: Zero build-step fragility, sub-second test suite execution, full offline/local container portability, and clean separation between domain logic and HTTP/SQLite adapters.
- **Negative / Trade-offs**: High-concurrency multi-writer deployments (>100 concurrent writes/sec) would require swapping `SqliteBoardgameRepository` for a PostgreSQL adapter implementing `BoardgameRepositoryPort`.

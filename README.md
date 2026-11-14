# Boardgame Page — Documentation & E2E Test Suite (`boardgame_page_docs`)

Companion documentation, Product & Software Design Documents (PRD/SDD), architecture diagrams, rule flowcharts, Docker Compose stack, and Behaviour-Driven Development (BDD) end-to-end test suite for [`lumenconsultancyae/Boardgame-page`](https://github.com/lumenconsultancyae/Boardgame-page).

## Documentation Index

- **Product & Architecture Specifications**:
  - [Product Requirements Document (PRD)](docs/PRD.md)
  - [Software Design Document (SDD)](docs/SDD.md)
  - [ADR 0001: Layered Architecture & Diagram Engine](docs/adr/0001-layered-architecture-and-diagram-engine.md)
- **User & Reference Guides**:
  - [End-User Getting Started Guide](docs/user-guide/getting-started.md)
  - [API & Operator Reference Guide](docs/reference/api-reference.md)
  - [Release Notes](docs/release-notes.md)
- **Deployment & BDD Verification**:
  - [Docker Compose Stack (`docker-compose.yml`)](docker-compose.yml)
  - [Behave BDD Feature Specifications (`features/boardgame_hub.feature`)](features/boardgame_hub.feature)

## Running the BDD End-to-End Test Suite

```bash
# Run all Gherkin scenarios against a running Boardgame Hub instance
behave -q --no-skipped features/
```

## Main Application Repository

- **Application Codebase**: [`lumenconsultancyae/Boardgame-page`](https://github.com/lumenconsultancyae/Boardgame-page)

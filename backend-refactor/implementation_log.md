# Implementation Log

- **Initial project review (30–60 min)**
  - Reviewed the project structure to understand the scope and existing issues.
  - Identified obsolete, duplicated, and unnecessary components.
  - Planned the workflow from the lowest layers (models) to the highest (routes and tests).

- **Technology and architecture decisions (10–20 min)**
  - Selected SQLAlchemy, Pydantic, and FastAPI based on project needs and familiarity.
  - Established a layered architecture (models → repositories → services → API).

- **Model refactoring (45–60 min)**
  - Rewrote ORM models with proper relationships and consistent structure.
  - Removed legacy fields from the old JSON-based version.
  - Prepared the data model for a future production-ready environment.

- **Schema creation and adjustments (30–45 min)**
  - Implemented create, update, and response schemas for each entity.
  - Refined fields as routing and business logic evolved.

- **Repository layer implementation (30–45 min)**
  - Created a repository layer to isolate database operations.
  - Moved CRUD logic out of services and routes.

- **Service layer refactoring (45–60 min)**
  - Updated service classes to depend on repositories.
  - Centralized business logic and error handling.

- **Routes implementation and cleanup (60–90 min)**
  - Implemented API endpoints for Assets, Signals, and Measurements.
  - Added pagination and specific query operations.
  - Adjusted validations and field definitions along the way.

- **Legacy code cleanup (20–30 min)**
  - Removed outdated, duplicated, or unused functions.
  - Improved naming, consistency, and structure throughout the codebase.

- **Database migration (20–30 min)**
  - Switched the local database from SQLite to PostgreSQL to better match production.
  - Updated settings and connection configuration.

- **Dockerization (20–30 min)**
  - Added Dockerfiles and Docker Compose setup for backend and database.
  - Organized environment variables and ensured containers ran smoothly.

- **Testing strategy definition (20–30 min)**
  - Chose to focus on integration tests due to time constraints.
  - Configured SQLite in-memory for fast, isolated testing.

- **Integration tests implementation (60–90 min)**
  - Set up test configuration (conftest, dependency overrides, FastAPI test client).
  - Wrote integration tests for main entities and endpoints.
  - Verified full end-to-end behavior from API to database.

---

### **Total estimated time: ~6–8 hours**

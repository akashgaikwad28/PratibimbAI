# Architecture Overview

PratibimbAI follows a **Service-Oriented Domain Architecture** designed for high reliability and ease of extension.

## Layered Design

### 1. API Layer (`app/api/`)
- Purely handles HTTP requests/responses.
- Validates input using Pydantic schemas.
- Enqueues heavy workloads to the background via `orchestration/queue.py`.

### 2. Orchestration Layer (`app/services/orchestration/`)
- Manages the lifecycle of agentic jobs.
- The `agent.py` acts as the entry point for LangGraph execution.
- `scheduler.py` handles periodic content monitoring.

### 3. Agent Layer (`app/graph/`)
- **LangGraph**: Used to define a stateful directed graph for the AI logic.
- **Wrappers**: Uses `@retry_node` to add resilience against transient failures.
- **State**: The `GraphState` object carries context throughout the pipeline.

### 4. Service Domain Layer (`app/services/`)
- **Ingestion**: Tools for fetching data from the web (Playwright, YouTube, HTTPX).
- **Processing**: Intelligence services like Vector Embeddings and LLM Ranking.
- **LLM**: A factory-based abstraction for interacting with different providers.

### 5. Data Layer
- **Repository**: Abstracted data access via `jobs/repository.py`.
- **Database Service**: Low-level query logic in `services/database/queries.py`.
- **Supabase**: Primary persistent store.
- **Redis**: Fast caching and job queue storage.

## Data Flow (Generation Job)

1. **User** submits request to `/generate`.
2. **API** creates a `pending` job in Supabase and enqueues to Redis.
3. **Worker** picks up the job and calls `orchestration/agent.py`.
4. **Agent** initializes the LangGraph and invokes the starting node.
5. **Graph** executes 8 nodes (Collect -> Clean -> Rank -> Memory -> Hook -> Write -> Critic -> Verify).
6. **Final Result** is saved back to Supabase and the job status is marked `completed`.

# 📄 PratibimbAI: System Architecture & Technical Documentation

Welcome to the official technical documentation for **PratibimbAI**. This document serves as a comprehensive guide for developers, architects, and stakeholders to understand the inner workings of our AI-driven content automation platform.

---

## 1. Project Overview
**PratibimbAI** (meaning "Reflection AI") is an automated content monitoring and social media generation platform. 

**The Problem:** Content creators and marketing teams spend hours manually scouring websites, blogs, and YouTube channels to find topics to post about. 
**The Solution:** PratibimbAI automates the "Research-to-Draft" pipeline. It monitors chosen sources, detects new content, extracts insights using AI agents, and drafts context-aware social media posts in the user’s unique "reflection" (style and profession).

---

## 2. Product Vision
Our goal is to create the "Autopilot" for digital presence.
*   **Passive Input**: Users simply "Connect" a source once.
*   **Active Monitoring**: The system works in the background 24/7.
*   **Intelligent Output**: The AI doesn't just summarize; it reshapes information into viral formats for LinkedIn, X (Twitter), and Instagram, maintaining the authority of the user's specific profession.

---

## 3. System Architecture
PratibimbAI is built using a modern **Decoupled Monolith** architecture with a clear separation between the AI graph logic and the API delivery layer.

### High-Level Architecture
1.  **Frontend (Next.js)**: A high-end, responsive dashboard for managing sources, viewing history, and triggering manual generations.
2.  **Backend (FastAPI)**: The orchestration layer handling auth, database persistence, and long-running background tasks.
3.  **Agent System (LangGraph)**: The "Brain" of the operation, executing a directed acyclic graph (DAG) of AI operations.
4.  **Database (Supabase)**: Handles User Auth, Profiles, Job Persistence, and Source Watchlists.
5.  **Background Services**: A dedicated async scheduler that polls external sources (Web/YouTube).

**Data Flow**:
`User/Scheduler` → `API` → `PostgreSQL (Job Created)` → `LangGraph Agent` → `LLM processing` → `PostgreSQL (Job Updated)` → `Frontend (Real-time Polling)`.

---

## 4. Agent Architecture (LangGraph)
The core of our intelligence is implemented using **LangGraph**, which provides persistent, stateful orchestration of LLM calls.

### The Graph Nodes
*   **`collect_node`**: 
    *   **Input**: List of URLs from State.
    *   **Action**: Iterates through URLs. Uses the `Scraper Service` for HTML and the `YouTube Service` for transcripts.
    *   **Output**: Updates `raw_contents`.
*   **`clean_node`**: 
    *   **Input**: `raw_contents`.
    *   **Action**: Uses `BeautifulSoup` to strip HTML tags, script blocks, and irrelevant noise. Truncates text to prevent context window overflow.
    *   **Output**: Updates `clean_contents`.
*   **`rank_node`**: 
    *   **Input**: `clean_contents` + `topic`.
    *   **Action**: Asks an LLM to identify the most relevant 3 sections from the gathered research.
    *   **Fallback**: If the LLM fails, it triggers the `heuristic_rank_node` which uses a snippet-based extraction logic.
    *   **Output**: Updates `ranked_contents`.
*   **`write_node`**: 
    *   **Input**: `ranked_contents` + User Preferences (Tone, Style, Profession).
    *   **Action**: Loads the `content_gen.txt` prompt and generates multiple post variations.
    *   **Output**: Updates `final_posts`.

---

## 5. LangGraph State Design
The `GraphState` object (defined in `state.py`) is the single source of truth that travels through the graph.

| Field | Type | Description |
| :--- | :--- | :--- |
| `topic` | `str` | The primary theme or update detected. |
| `urls` | `List[str]` | The sources to be analyzed. |
| `tone/style` | `str` | User-defined voice preferences. |
| `raw_contents` | `List[str]` | Unprocessed data from scrapers. |
| `clean_contents`| `List[str]` | Sanitized, LLM-ready text. |
| `ranked_contents`| `List[str]` | Filtered high-signal insights. |
| `final_posts` | `List[str]` | The final generated drafts. |
| `execution_id` | `uuid` | Tracking ID for logs and troubleshooting. |

**State Transitions**: Transitions are linear (`collect` → `clean` → `rank` → `write`). However, the `rank` node has conditional logic to handle provider failures via fallbacks.

---

## 6. Backend Architecture
The backend is organized for modularity and scalability.

```
app/
├── api/             # HTTP routes and Pydantic schemas
├── graph/           # LangGraph nodes, state, and graph definition
├── services/        # Third-party integrations (LLM, Scraping)
├── utils/           # Shared logic (Logging, Auth, Prompt Loading)
├── prompts/         # Version-controlled txt prompts
└── main.py          # Application entry point & Scheduler start
```
*   **`main.py`**: Initializes FastAPI and launches the `Scheduler` as a background task.
*   **`routes.py`**: Handles incoming requests, verifies JWTs, and hand-offs work to the Agent.

---

## 7. Services Layer
Our services are isolated to make future upgrades easy (e.g., swapping a scraper).

*   **Web Scraper**: Built on `requests` and `BeautifulSoup`. It mimics real browsers to avoid 403 Forbidden errors.
*   **YouTube Loader**: Uses `youtube-transcript-api` to convert video IDs into searchable text.
*   **Logging System**: A custom wrapper around Python’s `logging` that includes `execution_id` in every line, making it easy to trace a single request through the whole system.

---

## 8. LLM System & Multi-Provider Strategy
PratibimbAI is **Model-Agnostic**. We use a **Factory Pattern** (`llm/factory.py`) to instantiate clients.

### Supported Providers:
1.  **Groq**: Used for high-speed, cost-effective processing.
2.  **Gemini**: Used for deep reasoning and handling large context windows.
3.  **OpenAI**: Used as the platinum standard for creative writing.

### Fallback & Prioritization:
The system checks for API keys in this order:
1.  **User-Provided Key**: Fetched from the user's Supabase profile.
2.  **System Environment Key**: The project’s default keys.
3.  **Heuristic Fallback**: If LLM generation fails entirely, the system produces a "Basic Update" based on scraped snippets so the user isn't left empty-handed.

---

## 9. Prompt System
Prompts are stored as `.txt` files in `backend/app/prompts/`. 

**Why separate files?**
*   **Clean Code**: Avoids messy, multi-line strings in Python files.
*   **Collaboration**: Non-developers can tweak AI behavior without touching logic.
*   **Variable Injection**: We use `{{tags}}` for dynamic replacement of topic, tone, and style.

---

## 10. Data Flow Example
**Scenario**: User monitors a YouTube link and asks for a professional LinkedIn post.

1.  **Trigger**: The Background Scheduler detects a new transcript hash.
2.  **Hand-off**: The Scheduler calls `run_agent(job_id, request)`.
3.  **Collection**: `collect_node` pulls the 15-minute transcript.
4.  **Sanitization**: `clean_node` removes timestamps and [Music] tags.
5.  **Ranking**: `rank_node` identifies 3 core professional insights.
6.  **Writing**: `write_node` creates 3 LinkedIn-formatted drafts using the user's "AI Researcher" profession context.
7.  **Delivery**: The UI updates automatically via polling to show the finished cards.

---

## 11. Error Handling
We follow a **"Fail-Safe"** philosophy.
*   **Scraping Failures**: If one URL fails, the system continues with the others.
*   **LLM Rate Limits**: The `rank` node switches to a heuristic ranker if the LLM provider returns a 429 error.
*   **Graceful Degradation**: Every job has a `status` (PENDING, RUNNING, COMPLETED, FAILED). If a job fails, the user sees a specific error message rather than a spinning loader.

---

## 12. Logging and Observability
We use **Prefixed Logging**. Every log entry begins with `[execution_id]`.
*   **Tracing**: You can grep all logs for a specific job ID to see exactly where it slowed down or failed.
*   **Metrics**: We use custom decorators (`@instrument_node`) to measure the time taken by each agent step, identifying bottlenecks in scrapers or models.

---

## 13. Security Design
*   **Authentication**: Handled via **Supabase Auth** (JWT). The backend validates tokens on every request.
*   **User API Keys**: Keys are stored in the `profiles` table in Supabase. They are never sent to the frontend; the backend fetches them directly when running the agent.
*   **RLS (Row Level Security)**: Database policies ensure User A cannot see the sources or history of User B.

---

## 14. Performance Considerations
*   **Hashing**: We use MD5 content hashes to avoid re-polling if content hasn't changed.
*   **Content Truncation**: Text is capped at 5000 chars before LLM submission to minimize token costs and latency.
*   **Async Processing**: All scrapers and AI calls run as non-blocking background tasks.

---

## 15. Future Improvements
1.  **Vector Database (RAG)**: Store all scraped content in a vector db (like Pinecone or Supabase Vector) to allow the agent to reference historical updates.
2.  **Trending Topic Detection**: Integrate an agent that scans Google Trends or X Trends to "recommend" sources.
3.  **Self-Review Agent**: Add a node after `write_node` that "critiques" the post for SEO and viral potential before showing it to the user.
4.  **Auto-Scheduling**: Directly post to LinkedIn/X via their APIs once the user approves a draft.

---

## 16. Deployment Architecture
*   **Backend**: Render or Heroku (Dockerized).
*   **Frontend**: Vercel (Next.js Edge Runtime).
*   **Database/Auth**: Supabase.
*   **Environment**: Secrets managed via `.env` (backend) and Vercel dashboard (frontend).

---

## 17. Scaling Strategy
*   **Worker Queues**: If we scale to thousands of users, we would move from FastAPI background tasks to a dedicated task queue like **Celery** with **Redis**.
*   **Database Indexing**: Add indexes on `user_id` and `last_polled_at` to handle millions of sources efficiently.
*   **Load Balancing**: Deploy multiple backend instances behind an Nginx load balancer to handle concurrent LLM streams.

---

## 18. Startup Potential (SaaS)
PratibimbAI has high commercial viability as a B2B SaaS tool.
*   **Enterprise Tier**: Features like "Team Collaboration" and "Multi-Brand Profiles."
*   **White-Labeling**: Allow agencies to use the agent engine for their own clients.
*   **Premium Connectors**: Specialized scrapers for gated content like pays-walled newsletters or academic journals.

---
**Documentation generated on 2026-03-06**
**Lead Architect: PratibimbAI Dev Team**

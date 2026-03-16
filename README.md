# PressW — LLM-Powered Cooking & Recipe Q&A

Monorepo for the PressW intern technical assessment: **AI-powered recipe chatbot** (LangChain + LangGraph) with a **Next.js** chat frontend.

## Structure

```
.
├── backend/          # FastAPI + LangGraph
├── frontend/         # Next.js (App Router) + TypeScript + Tailwind
├── docker-compose.yml
└── README.md
```

## Local setup

### Prerequisites

- Python 3.11+
- Node 20+ (or Bun / pnpm)
- (Optional) Docker Desktop for `docker compose up`

### Without Docker

**Backend:**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # or: .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp ../.env.example .env     # then add your OPENAI_API_KEY etc.
uvicorn main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
bun install   # or: pnpm install
bun run dev   # or: pnpm dev
```

Open [http://localhost:3000](http://localhost:3000). Backend at [http://localhost:8000](http://localhost:8000).

### With Docker

```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY (and SERP_API_KEY if used)
docker compose up --build
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)

## Environment variables

See [.env.example](.env.example). Documented keys:

- `OPENAI_API_KEY` — required for LLM (LangChain).
- `SERP_API_KEY` — optional, for web/search tool.
- `NEXT_PUBLIC_API_URL` — frontend API base URL (e.g. `http://localhost:8000`).

## Status

- Scaffolding and first commit done.
- Backend: stub FastAPI + health check; LangGraph and tools to be added.
- Frontend: minimal Next.js page; chat UI to be added.

## License

Private — PressW intern assessment.

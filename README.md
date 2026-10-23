# Multi-Agent Research Assistant

A FastAPI service that plans technical research, retrieves web and academic evidence, reviews findings, and produces a referenced report through a six-node LangGraph workflow.

## Problem and approach

Developers, students, and technical researchers need relevant sources and a synthesis of competing findings. This assistant separates source selection, evidence gathering, review, and writing so intermediate decisions can be inspected alongside the final report.

All nodes use the same configured GPT-4o model at temperature 0. They are specialized workflow stages, rather than independently trained models.

## Architecture

| Stage | Implementation |
| --- | --- |
| Planner | Generates a research plan and routing flags, validated with Pydantic. |
| Web research | Generates search queries and calls Tavily, requesting three results per query. |
| Paper research | Generates up to three queries and retrieves up to three arXiv results per query. Supplies title, authors, date, and a truncated abstract. |
| Verification | Uses the model to review retrieved findings and identify conflicts. |
| Summarization | Combines evidence and review notes into structured notes. |
| Report | Produces the final report, including findings, uncertainty, and requested references. |

A typed state carries the question, plan, routing flags, evidence, and intermediate outputs.

| Selected sources | Execution after planning |
| --- | --- |
| Web only | Web research → verification → summary → report |
| Papers only | Paper research → verification → summary → report |
| Both | Web research → paper research → verification → summary → report |

The combined route is sequential. If both planner flags are false, the current router falls back to both sources.

Compared with one-call synthesis, this design exposes intermediate evidence and review decisions and can skip an unnecessary source type. Additional model calls introduce latency and cost; a quality advantage over a simpler baseline has not been established by the supplied application files.

## Files

| Path | Purpose |
| --- | --- |
| `app/main.py` | FastAPI endpoints |
| `app/workflow.py` | Graph construction and routing |
| `app/state.py`, `app/models.py` | Workflow state and output schemas |
| `app/config.py`, `app/logging_config.py` | Model configuration and logging |
| `app/agents/` | Six workflow nodes |
| `app/tools/arxiv_search.py` | Academic search helper |
| `requirements.txt` | Runtime dependencies |
| `Dockerfile`, `docker-compose.yml` | Container setup |
| `.env.example` | Credential configuration template |

## Run locally

Use Python 3.12 and configure both API keys before starting the server.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Set `OPENAI_API_KEY` and `TAVILY_API_KEY` in `.env`.

```bash
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs> for interactive API documentation.

```bash
curl -X POST http://127.0.0.1:8000/research \
  -H 'Content-Type: application/json' \
  -d '{"question":"What are the tradeoffs between RAG and fine-tuning?"}'
```

The response contains workflow state, including `report`, `plan`, retrieved evidence, verification notes, and summary. `GET /` returns the service name; `GET /health` returns process status without testing external providers.

Live requests require access to OpenAI, Tavily, and arXiv. OpenAI and Tavily usage can incur charges.

## Docker

```bash
docker build -t multiagent-research-api .
docker run --rm -p 8000:8000 --env-file .env multiagent-research-api
```

Alternatively:

```bash
docker compose up --build
```

Stop Compose with `docker compose down`. Credentials are provided at runtime and excluded from the image.

## Reliability and evaluation

Search nodes catch individual query errors and retain them in the workflow state. Stage logging writes to the console and `research_assistant.log`; generated logs are ignored by Git. Several nodes print model usage metadata, but this is not consolidated token, cost, or stage-duration accounting.

The supplied historical documentation describes a synthetic one-call versus three-step synthesis comparison and a separate five-question exploratory model-judge experiment. Their evaluation code and reproducible datasets are not included in these application modules. They do not establish an accuracy improvement for this service. No benchmark or passing-test totals are claimed here.

## Limitations

- Verification is an LLM review of retrieved evidence, not an independent fact-checking guarantee.
- Paper retrieval uses abstracts and omits canonical paper URLs and identifiers from its formatted output. References requested by the report prompt are not programmatically validated.
- Structured query parsing can fail; the API surfaces workflow exceptions as HTTP 500 responses.
- Empty or irrelevant search results are not automatically retried or filtered for relevance.
- The graph has no persistent checkpointer or resume mechanism.
- There are no application-level authentication controls or explicit request/token budgets.
- Repeated evidence across synthesis stages increases context size and cost.
- Dependency installation, Docker execution, and live provider calls require separate runtime verification.

Next improvements are source-grounded citation checks, a paired one-call baseline, bounded retries, persistent execution state, and per-stage usage measurements.

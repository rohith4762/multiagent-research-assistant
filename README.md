# Multi-Agent Research Assistant

> Autonomous 6-agent AI research pipeline built with LangGraph — achieving **faithfulness of 0.84** and **answer relevancy of 0.82** evaluated across 5 diverse research domains using LLM-as-judge.

---

## What This Project Does

Given any research question, this system automatically:

1. **Plans** a research strategy tailored to the query
2. **Searches** the web for current information using Tavily
3. **Finds** relevant academic papers using ArXiv API
4. **Verifies** accuracy by cross-checking all sources
5. **Summarizes** findings into structured notes
6. **Generates** a professional research report with citations

**Example input:**
> "What are the latest advances in Retrieval Augmented Generation?"

**Example output:** A structured research report with executive summary, key findings, academic citations from ArXiv, industry comparisons, and uncertainty analysis.

---

## Architecture

```
User Query
     ↓
Planner Agent
(analyzes query, creates research plan,
 decides which agents to activate)
     ↓
┌────────────────────────────────┐
│                                │
Research Agent          Paper Agent
(Tavily web search)     (ArXiv academic papers)
│                                │
└──────────────┬─────────────────┘
               ↓
      Verification Agent
      (cross-checks accuracy,
       identifies conflicts)
               ↓
      Summarization Agent
      (combines all findings
       into structured notes)
               ↓
        Report Agent
   (generates final professional
    report with citations)
               ↓
      Final Research Report
```

### Key Design Decisions

**Dynamic Conditional Routing:** The Planner agent decides at runtime whether to activate web search, academic paper search, or both — based on the nature of the query. Technical questions activate both agents. Factual queries may use only web search.

**Pydantic Structured Outputs:** Every agent uses Pydantic models to validate LLM responses before passing them downstream. This prevents malformed data from crashing the pipeline.

**Graceful Error Handling:** Each agent wraps external API calls in try/except blocks. If ArXiv is slow or Tavily returns no results, the pipeline continues with available data rather than crashing.

**Comprehensive Logging:** Every agent logs start, completion, token usage, and API latency — enabling production monitoring and debugging.

---

## Evaluation Results

Evaluated using LLM-as-judge methodology across 5 diverse research domains:

| Question Domain | Faithfulness | Answer Relevancy |
|---|---|---|
| RAG advances | 0.80 | 0.90 |
| QLoRA vs fine-tuning | 0.90 | 0.80 |
| Multi-agent challenges | 0.80 | 0.90 |
| Vector databases | 0.80 | 0.70 |
| RAG vs fine-tuning tradeoffs | 0.90 | 0.80 |
| **Average** | **0.84** | **0.82** |

**Faithfulness (0.84):** Reports contain factually accurate, grounded information 84% of the time.

**Answer Relevancy (0.82):** Reports directly answer the research question asked 82% of the time.

---

## Tech Stack

| Component | Technology |
|---|---|
| Agent Orchestration | LangGraph |
| LLM Framework | LangChain |
| Language Model | OpenAI GPT-4o |
| Web Search | Tavily Search API |
| Academic Papers | ArXiv API |
| Structured Outputs | Pydantic v2 |
| State Management | LangGraph TypedDict State |
| Logging | Python logging module |

---

## Agent Details

### 1. Planner Agent
- Analyzes the research question
- Creates a step-by-step research plan
- Decides which downstream agents to activate
- Returns structured `PlannerOutput` with plan, `use_research`, and `use_paper` flags

### 2. Research Agent
- Uses Tavily Search to find current web information
- Searches technical blogs, documentation, and industry sources
- Returns structured list of search results with sources

### 3. Paper Agent
- Uses ArXiv API to find academic research papers
- Generates multiple search queries based on the research plan
- Extracts paper titles, authors, publication dates, and summaries

### 4. Verification Agent
- Cross-checks findings from Research and Paper agents
- Identifies conflicting information across sources
- Flags uncertainty where sources disagree

### 5. Summarization Agent
- Combines verified findings into structured notes
- Maintains source attribution throughout
- Prepares organized content for the Report agent

### 6. Report Agent
- Generates professional research reports in structured format
- Includes: Executive Summary, Key Findings, Academic Research, Industry Comparison, Uncertainty Analysis, Conclusion, and References
- Suitable for technical and non-technical audiences

---

## Sample Output

**Query:** "What are the latest advances in Retrieval Augmented Generation?"

**Report excerpt:**
```
## Executive Summary
Retrieval Augmented Generation (RAG) has seen substantial growth 
since 2021, with notable advancements including Rich Answer Encoding 
(RAE), GenRT, and Self-CRAG improving retrieval relevance, utility, 
and factual consistency. Academic contributions like AR-RAG and 
FAIR-RAG have expanded RAG applications to complex multi-hop queries.

## Key Findings
1. Rich Answer Encoding (RAE): Improves retrieval by embedding 
   answer-aligned semantics (Huang et al., 2023)
2. FAIR-RAG: Introduces evidence-driven reasoning for multi-hop 
   queries (Asl et al., 2025)
3. RAG-Star: Integrates tree-based deliberative reasoning 
   (Jiang et al., 2024)

## Academic Research
[ArXiv citations with real paper references...]
```

---

## Setup and Installation

### Prerequisites
- Python 3.11+
- OpenAI API key
- Tavily API key

### Installation

```bash
# Clone the repository
git clone https://github.com/rohith4762/multi-agent-research-assistant
cd multi-agent-research-assistant

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys to .env
```

### Environment Variables

Create a `.env` file with:

```
OPENAI_API_KEY=your-openai-api-key
TAVILY_API_KEY=your-tavily-api-key
```

### Running the Project

Open `multiagent.ipynb` in Jupyter or VS Code and run all cells.

To ask a research question:

```python
result = app.invoke({
    "question": "What are the latest advances in Retrieval Augmented Generation?"
})
print(result["report"])
```

---

## Project Structure

```
multi-agent-research-assistant/
├── multiagent.ipynb      # Main notebook with all agents
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

---

## Key Technical Features

**LangGraph StateGraph:** All 6 agents share a typed state object. Each agent reads from and writes to state — enabling clean data flow without global variables.

**Conditional Routing:** `route_after_planner` function dynamically decides the next agent based on the Planner's structured output. If `use_paper=False`, the Paper agent is skipped entirely.

**ArXiv Integration:** Custom ArXiv client with configurable page size, retry logic, and delay seconds to respect rate limits. Searches multiple queries per question for comprehensive coverage.

**Token Usage Logging:** Every LLM call logs input tokens, output tokens, and total tokens — enabling cost monitoring in production.

---

## Author

**Rohith Muppi**
MS Data Science, University of Alabama at Birmingham (GPA: 3.80/4.0)
Authorized to work in the US on OPT — no employer sponsorship required.

- GitHub: [github.com/rohith4762](https://github.com/rohith4762)
- LinkedIn: [linkedin.com/in/rohith-muppi-27921a23b](https://linkedin.com/in/rohith-muppi-27921a23b)
- Email: muppirohith@gmail.com

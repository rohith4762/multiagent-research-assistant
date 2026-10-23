import json
from langchain_core.messages import SystemMessage, HumanMessage

from app.config import llm
from app.logging_config import logger
from app.models import PlannerOutput
from app.state import State


def planner_agent(state: State):

    logger.info("planner_agent just started")

    messages = [

        SystemMessage(content="""
You are an AI Research Planning Agent.

Your responsibility is to analyze the user's research question
and create a clear research plan.

Break the question into smaller research tasks that can be
completed by specialized agents.

Available agents:

1. Research Agent
   - searches technical blogs, documentation, and web sources.

2. Paper Agent
   - finds and analyzes academic research papers.

3. Verification Agent
   - checks information accuracy across sources.

4. Summarization Agent
   - combines findings into structured notes.

5. Report Agent
   - generates the final research report.

Decide whether web research and academic paper research
are needed.

Return ONLY valid JSON in exactly this format:

{
    "plan": "Detailed step-by-step research plan",
    "use_research": true,
    "use_paper": false
}

Rules:

- use_research should be true if web sources,
  documentation, blogs, or current technical information
  are useful.

- use_paper should be true if academic research papers,
  scientific evidence, algorithms, or research findings
  are useful.

- Both can be true.

- Do not answer the user's question.
- Only create the research workflow plan.
        """),

        HumanMessage(
            content=state["question"]
        )
    ]

    response = llm.invoke(messages)

    print("MODEL RESPONSE:")
    print(response.content)

    logger.info("planner_agent completed")


    content = response.content.strip()


    if content.startswith("```json"):
        content = content[7:]

    elif content.startswith("```"):
        content = content[3:]

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()


    data = json.loads(content)


    planner_output = PlannerOutput(**data)

    return {
        "plan": planner_output.plan,
        "use_research": planner_output.use_research,
        "use_paper": planner_output.use_paper
    }

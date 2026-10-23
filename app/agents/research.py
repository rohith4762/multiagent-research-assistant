from langchain_core.messages import SystemMessage, HumanMessage
from langchain_tavily import TavilySearch

from app.config import llm
from app.logging_config import logger
from app.models import strc
from app.state import State


tools=TavilySearch(max_results=3)

def Research_agent(state: State):
    logger.info("Research_agent just started")
    messages=[

        SystemMessage(content="""
            You are an AI Research Agent.

            Your responsibility is to gather information from various sources based on the research plan provided by the Planner Agent.

            Use the TavilySearch tool to find relevant information from technical blogs, documentation, and web sources.

            Collect important concepts, industry updates, and any other relevant information.

            Do not answer the user's question directly.
            Only gather information as per the research plan.

            Example:

            Research Plan:
            "Find recent blogs and technical articles about RAG techniques."

            Output:
            - Collected information from various sources.
            - Key concepts and industry updates related to RAG techniques.
            """
        ),
        HumanMessage(content=f"{state['question']} and you can refer to the plan {state['plan']} for guidance on what to research. Please provide a summary of your findings.")
    ]
    print(state['question'])

    response=llm.with_structured_output(strc,include_raw=True).invoke(messages)
    results = []

    for query in response['parsed'].quries:

        try:

            search_results = tools.run(
                query
            )

            results.append({
                "query": query,
                "results": search_results
            })

        except Exception as e:

            logger.exception(
                f"Search failed for query: {query}"
            )

            results.append({
                "query": query,
                "error": str(e)
            })

    logger.info(
        f"Research_agent completed with "
        f"{len(results)} results"
    )

    return {
        "research": results
    }

from langchain_core.messages import SystemMessage, HumanMessage

from app.config import llm
from app.logging_config import logger
from app.models import strc
from app.state import State
from app.tools.arxiv_search import search_arxiv


def Paper_agent(state: State):
    logger.info("Paper_agent just started")
    messages=[

        SystemMessage(content="""
            You are an AI Paper Agent.

            Your responsibility is to find and analyze academic research papers based on the research plan provided by the Planner Agent.

            Use the Arxiv tool to find relevant academic papers.

            Extract key contributions, methodologies, and findings from the papers.

            Do not answer the user's question directly.
            Only gather information as per the research plan.

            Example:

            Research Plan:
            "Find recent research papers about RAG improvements."

            Output:
            - Collected information from various academic papers.
            - Key contributions and findings related to RAG techniques.
            """
        ),
        HumanMessage(content=f"{state['question']} and you can refer to the plan {state['plan']} for guidance on what to research. Please provide a summary of your findings.")
    ]

    output=llm.with_structured_output(strc,include_raw=True).invoke(messages)
    print(output["raw"].usage_metadata)

    op=[]

    for query in output['parsed'].quries[:3]:
        try:

            sr = search_arxiv(
                query
            )

            op.append({
                "query": query,
                "results": sr
            })

        except Exception as e:

            logger.exception(
                f"arXiv search failed: {query}"
            )

            op.append({
                "query": query,
                "error": str(e)
            })

    logger.info(
        f"Paper_agent completed with "
        f"{len(op)} results"
    )
    return{
        "paper":op

    }

from langchain_core.messages import SystemMessage, HumanMessage

from app.config import llm
from app.logging_config import logger
from app.state import State


def Report_agent(state: State):
    logger.info("generating final report")
    messages = [
        SystemMessage(content="""
            You are an AI Report Generation Agent.

            Your responsibility is to write a final, professional research report
            based on the structured summary notes provided.

            Structure the report with these sections:
            1. Executive Summary — a short, high-level overview (3-5 sentences).
            2. Key Findings — the main concepts and developments, organized clearly.
            3. Academic Research — contributions and findings from academic papers.
            4. Technology / Industry Comparison — if applicable, compare approaches or tools discussed.
            5. Points of Uncertainty or Disagreement — where sources conflicted or coverage was thin.
            6. Conclusion — a brief closing synthesis.

            Write in clear, professional prose suitable for sharing with a
            technical audience. Do not introduce facts that are not present in
            the provided summary notes.
        """),
        HumanMessage(content=f"""
            Original question: {state['question']}

            Summary notes:
            {state['summary']}

            Please write the final report.
            before giving the final report please check all info like {state.get('research', [])} and {state.get('paper', [])} and {state.get('verification_task', '')} and {state['summary']} and give the final report.
            and also include the references of the papers and blogs used in the report.also provide the research papers and blogs used in the report in the references section of the report.
        """)
    ]

    response = llm.invoke(messages)
    print(response.usage_metadata)
    print(response.content)
    logger.info("final report completed")

    return {
        "report": response.content
    }

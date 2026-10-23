from langchain_core.messages import SystemMessage, HumanMessage

from app.config import llm
from app.logging_config import logger
from app.state import State


def summarization_agent(state: State):
    logger.info("summarization_agent just started")
    messages3=[

        SystemMessage(content="""
            You are an AI Summarization Agent.

            Your responsibility is to combine the findings from the Research, Paper, and Verification Agents into structured notes.

            Create a clear and concise summary of the information gathered.

            Do not answer the user's question directly.
            Only summarize the information as per the research plan.

            Example:

            Research Plan:
            "Summarize the findings  about the question"

            Output:
            - Structured notes summarizing the key points from all sources.
            """
        ),
        HumanMessage(content=f"{state['question']} and you can refer to the plan {state['plan']} for guidance on what to summarize. Please provide a summary of your findings. and you can refer to the research findings {state.get('research', [])} and paper findings {state.get('paper', [])} for comparison. and moreover you can also refer to the verification findings for more information{state.get('verification_task', '')}. Please provide a structured summary of all the information gathered.")
    ]
    response=llm.invoke(messages3)
    print(response.usage_metadata)
    logger.info("summarization_agent ended")

    return{
        "summary":response.content
    }

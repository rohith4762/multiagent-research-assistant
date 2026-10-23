from langchain_core.messages import SystemMessage, HumanMessage

from app.config import llm
from app.logging_config import logger
from app.state import State


def Verfication_agent(state: State):
    logger.info("Verfication_agent just started")
    messages2=[

        SystemMessage(content="""
            You are an AI Verification Agent.

            Your responsibility is to check the accuracy of the information gathered by the Research and Paper Agents.

            Compare findings from multiple sources and identify any conflicting information.

            Ensure that the information is reliable and accurate.

            Do not answer the user's question directly.
            Only verify the information as per the research plan.

            Example:

            Research Plan:
            "Verify the accuracy of information about RAG techniques."

            Output:
            - Verified information from various sources.
            - Identified any conflicting information.
            """
        ),
        HumanMessage(content=f"{state['question']} and you can refer to the plan {state['plan']} for guidance on what to verify. Please provide a summary of your findings. and you can refer to the research findings {state.get('research', [])} and paper findings {state.get('paper', [])} for comparison.verify all the information and also provide the mistakes if any and also provide the correct information if any mistakes are found.")
    ]
    respons=llm.invoke(messages2)
    print(respons.usage_metadata)



    print(respons.content)
    logger.info("Verfication_agent completed")

    return{
        "verification_task":respons.content
    }

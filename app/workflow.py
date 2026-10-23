from langgraph.graph import StateGraph, END

from app.state import State
from app.agents.planner import planner_agent
from app.agents.research import Research_agent
from app.agents.paper import Paper_agent
from app.agents.verification import Verfication_agent
from app.agents.summarization import summarization_agent
from app.agents.report import Report_agent


graph = StateGraph(State)


def route_after_planner(state: State):
    use_research = state.get("use_research", True)
    use_paper = state.get("use_paper", True)
    if use_research and use_paper:
        return "both"
    if use_research:
        return "research_only"
    if use_paper:
        return "paper_only"
    return "both"


def route_after_research(state: State):
    if state.get("use_paper", True):
        return "paper"
    return "verification"


graph = StateGraph(State)

graph.add_node("planner", planner_agent)
graph.add_node("research", Research_agent)
graph.add_node("paper", Paper_agent)
graph.add_node("verification", Verfication_agent)
graph.add_node("summary", summarization_agent)
graph.add_node("report", Report_agent)

graph.set_entry_point("planner")

graph.add_conditional_edges(
    "planner",
    route_after_planner,
    {
        "both": "research",
        "research_only": "research",
        "paper_only": "paper",
    }
)

graph.add_conditional_edges(
    "research",
    route_after_research,
    {
        "paper": "paper",
        "verification": "verification"
    }
)

graph.add_edge("paper", "verification")
graph.add_edge("verification", "summary")
graph.add_edge("summary", "report")
graph.add_edge("report", END)

app = graph.compile()

from typing import Annotated,TypedDict,List

class State(TypedDict):
    question: str
    plan:str
    research_task: str
    verification_task: str
    research: list
    paper: list
    summary: str
    report: str
    use_research: bool
    use_paper: bool

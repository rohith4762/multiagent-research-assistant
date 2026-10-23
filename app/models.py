from pydantic import BaseModel, Field
from typing import List

class strc(BaseModel):
    quries: List[str]


class PlannerOutput(BaseModel):

    plan: str = Field(
        description="Detailed research plan."
    )

    use_research: bool = Field(
        description="Whether the web Research Agent should be used."
    )

    use_paper: bool = Field(
        description="Whether the academic Paper Agent should be used."
    )


class SearchQueries(BaseModel):

    queries: List[str]

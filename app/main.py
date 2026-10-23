from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.workflow import app as research_app


app = FastAPI(
    title="Multi-Agent Research Assistant",
    version="1.0.0"
)


class ResearchRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "Multi-Agent Research Assistant API"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research")
def research(request: ResearchRequest):
    try:
        result = research_app.invoke({"question": request.question})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI
from pydantic import BaseModel
from app.server import Orchestrator

app = FastAPI(
    title="Company Research Assistant API",
    version="1.0"
)

orch = Orchestrator()

class CompanyRequest(BaseModel):
    company: str

@app.get("/")
def root():
    return {"message": "Company Research Assistant API is running!"}

@app.post("/generate_plan")
def generate_plan(req: CompanyRequest):
    result = orch.run_pipeline(req.company)
    return result

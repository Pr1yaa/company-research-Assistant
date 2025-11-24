from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.server import Orchestrator

app = FastAPI()
orch = Orchestrator()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/plan")
def generate_plan(data: dict):
    company = data.get("company")
    result = orch.run_pipeline(company)
    return result

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.chat_agent import ChatAgent

app = FastAPI()

# Create agent instance
agent = ChatAgent()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatPayload(BaseModel):
    message: str
    session_id: str

@app.post("/chat")
async def chat_endpoint(payload: ChatPayload):
    # Use the new method name: process_request
    reply = agent.process_request(payload.session_id, payload.message)
    return {"reply": reply}

@app.get("/")
async def root():
    return {"status": "running", "message": "Company Research Assistant API"}

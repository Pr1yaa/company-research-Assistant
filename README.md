# company-research-Assistant
# **Company Research Assistant — Account Plan Generator**

A production-grade, multi-agent conversational AI system designed to help users research companies and generate structured **Account Plans** through natural dialogue.
This project is built as part of the **Eightfold.ai — AI Agent Building Assignment**.

---

## 🔍 **Overview**

The Company Research Assistant enables users to:

* Conduct company research from multiple online sources
* Receive synthesized, concise business insights
* Generate complete account plans automatically
* Update or refine selected sections on demand
* Interact naturally through a chat interface
* Experience adaptive, persona-aware AI behaviour

The system prioritizes **conversational quality, agentic reasoning, error handling, and adaptability**.

---

## 🚀 **Key Capabilities**

### 🧠 Multi-Agent Intelligence

* **Planner Agent** — Identifies research subtasks
* **Researcher Agent** — Gathers company information
* **Summarizer Agent** — Condenses raw findings
* **Synthesizer Agent** — Produces the structured account plan

### 🗂️ Account Plan Structure

* Company Overview
* Leadership & Key Executives
* Business Units
* Market Position
* Risks & Challenges
* Opportunities
* Competitors
* Recommendations

### 🎭 Persona-Aware Adaptability

The agent dynamically adjusts behaviour for:

* **Efficient Users**
* **Confused Users**
* **Chatty Users**
* **Edge-Case Users** (invalid or noisy inputs)

### ⚠️ Conflict & Error Handling

* Detects conflicting information
* Requests clarification
* Validates user inputs
* Handles unrealistic or unsupported requests gracefully

---

## 🏗️ **Architecture**

The system is organized into modular components for clarity, scalability, and separation of concerns:

```
app/
├── agents/
│   ├── planner.py
│   ├── researcher.py
│   ├── summarizer.py
│   └── synthesizer.py
├── chat_agent.py       # Core orchestrator
├── server.py           # FastAPI backend
└── ui/
    ├── index.html      # Chat interface
    ├── styles.css
    └── script.js
```

### **Tech Stack**

* **Python 3.10+**
* **FastAPI** for backend APIs
* **HTML/CSS/JavaScript** for frontend
* **OpenAI-style prompt engineering** for agent behaviour

---

## ⚙️ **Setup & Installation**

### 1. Clone the repository

```
git clone <your-public-repo-url>
cd company_research_assistant
```

### 2. Create & activate virtual environment

```
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install required dependencies

```
pip install -r requirements.txt
```

### 4. Run the FastAPI server

```
uvicorn app.server:app --reload --port 8000
```

### 5. Launch the UI

Open in browser:

```
http://localhost:8000
```

---

## 🧪 **Testing Scenarios**

The agent is tested across multiple personas:

| Persona            | Behaviour              | Expected Agent Response    |
| ------------------ | ---------------------- | -------------------------- |
| **Confused User**  | Vague/unclear requests | Asks clarifying questions  |
| **Efficient User** | Wants quick answers    | Provides concise outputs   |
| **Chatty User**    | Goes off-topic         | Politely redirects         |
| **Edge-Case User** | Invalid/noisy inputs   | Graceful fallback handling |

---

## 🎯 **Design Decisions**

* Modular multi-agent design enables isolated logic and easy scalability
* JSON-structured outputs ensure consistent formatting
* Backend retains conversation context; UI remains stateless
* Clarification-first interaction model reduces hallucination risks
* Structured account plan template improves reliability

---


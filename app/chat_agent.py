import json
from typing import Dict, Any

from app.agents.planner import Planner
from app.agents.researcher import Researcher
from app.agents.critic import Critic
from app.agents.summarizer import Summarizer
from app.agents.synthesizer import Synthesizer


class ChatAgent:
    """
    Full pipeline:
    User → Planner → Researcher → Critic → Summarizer → Final answer
    """

    def __init__(self):
        self.planner = Planner()
        self.researcher = Researcher()
        self.critic = Critic()
        self.summarizer = Summarizer()
        self.synthesizer = Synthesizer()

        # memory per session
        self.sessions: Dict[str, Dict[str, Any]] = {}

    # ---------------------------------------------------------
    # Create new session
    # ---------------------------------------------------------
    def create_session(self, session_id: str):
        self.sessions[session_id] = {
            "company": None,
            "sections": [],
            "summaries": {},
            "raw_records": {},
            "last_section": None
        }

    # ---------------------------------------------------------
    # Process incoming user message
    # ---------------------------------------------------------
    def process_request(self, session_id: str, user_message: str):
        if session_id not in self.sessions:
            self.create_session(session_id)

        s = self.sessions[session_id]
        msg = user_message.lower().strip()

        # ---- Handle research command ----
        if msg.startswith("research"):
            return self._handle_research(session_id, user_message)

        # ---- “details”, “more”, etc. ----
        if msg in ["details", "more", "expand", "explain further"]:
            if not s["last_section"]:
                return "Which section should I expand?"
            return self._dig_deeper(s["last_section"], s)

        # ---- fallback chat handling ----
        return "I can help with competitor analysis, financials, risks, opportunities, or overview. Example: 'research Google competitors'."

    # ---------------------------------------------------------
    # Extract company + section from user message
    # ---------------------------------------------------------
    def _handle_research(self, session_id, full_msg: str):
        msg = full_msg.lower()
        words = msg.split()

        # ---- Detect company ----
        known = ["google", "amazon", "tesla", "microsoft", "meta", "apple"]
        company = None

        for w in words:
            if w in known:
                company = w
                break

        if not company:
            company = words[-1]  # fallback to last word

        # ---- Detect section ----
        if "competitor" in msg:
            section = "competitors"
        elif "financial" in msg:
            section = "financials"
        elif "risk" in msg:
            section = "risks"
        elif "opportunit" in msg:
            section = "opportunities"
        elif "overview" in msg:
            section = "overview"
        else:
            section = "overview"

        s = self.sessions[session_id]
        s["company"] = company
        s["sections"] = [section]

        return self._run_section_research(section, s)

    # ---------------------------------------------------------
    # RUN: Researcher → Critic → Summarizer
    # ---------------------------------------------------------
    def _run_section_research(self, section, s):

        task = {"task_id": f"task_{section}", "section": section}

        # ---- Step 1: Research ----
        research_out = self.researcher.run_task(s["company"], task)
        raw = research_out.get("raw_records", [])

        # ---- Step 2: Critic ----
        critic_out = self.critic.evaluate(task["task_id"], raw)
        validated = critic_out.get("validated_records", [])
        conf = critic_out.get("overall_confidence", 0.0)

        # ---- Step 3: Summarizer ----
        summary = self.summarizer.summarize_section(section, validated)

        # Save memory
        s["raw_records"][section] = validated
        s["summaries"][section] = summary
        s["last_section"] = section

        return f"{section.title()} (Confidence: {int(conf*100)}%)\n{summary}"

    # ---------------------------------------------------------
    # DEEPER RESEARCH
    # ---------------------------------------------------------
    def _dig_deeper(self, section, s):

        task = {"task_id": f"{section}_deep", "section": section}

        # new research
        new_out = self.researcher.run_task(s["company"], task)
        new_raw = new_out.get("raw_records", [])

        critic_new = self.critic.evaluate(task["task_id"], new_raw)
        validated_new = critic_new.get("validated_records", [])

        # append
        if section not in s["raw_records"]:
            s["raw_records"][section] = []

        s["raw_records"][section].extend(validated_new)

        # rebuild summary
        new_summary = self.summarizer.summarize_section(section, s["raw_records"][section])
        s["summaries"][section] = new_summary

        return f"Updated {section}:\n{new_summary}"

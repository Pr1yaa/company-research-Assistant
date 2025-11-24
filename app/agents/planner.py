import uuid
from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


SYSTEM_PROMPT = """
You are the PLANNER.

Your job:
1. Break the user's research request into structured sections.
2. Identify the company name.
3. Identify all analysis categories like:
   - overview
   - competitors
   - financials
   - opportunities
   - risks
   - products/services
   - market position
   - SWOT
4. Return a JSON list of sections.
5. Use only valid sections. No hallucinated categories.
6. If unclear, infer the most relevant sections.
"""

VALID_SECTIONS = [
    "overview",
    "competitors",
    "financials",
    "opportunities",
    "risks",
    "products",
    "market",
    "swot",
]


class Planner:

    def generate_plan(self, user_request):
        """
        user_request = {
            "company": "Google",
            "query": "research google competitors and risks"
        }
        """

        company = user_request.get("company")
        query = user_request.get("query")

        # -----------------------
        # Ask GPT to detect sections
        # -----------------------
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": (
                            f"User Query: {query}\n"
                            f"Company: {company}\n\n"
                            "Return only the list of sections needed."
                        )
                    }
                ]
            )

            detected = response.choices[0].message.content.lower()

            sections = []
            for sec in VALID_SECTIONS:
                if sec in detected:
                    sections.append(sec)

            if not sections:
                sections = ["overview"]

        except Exception:
            sections = ["overview"]

        # -----------------------
        # Create tasks
        # -----------------------
        tasks = []
        for i, sec in enumerate(sections, 1):
            tasks.append({
                "task_id": f"t{i}",
                "section": sec,
                "description": f"Collect raw data for {sec}"
            })

        return {
            "plan_id": f"plan_{uuid.uuid4().hex[:8]}",
            "company": company,
            "sections": sections,
            "tasks": tasks
        }

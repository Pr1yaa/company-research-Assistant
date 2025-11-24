import os
import requests
from openai import OpenAI

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SEARCH_URL = "https://google.serper.dev/search"


SYSTEM_PROMPT = """
You are an expert corporate analyst.

TASK:
1. Read messy web search results.
2. Extract ONLY factual insights about the company & section.
3. Remove only useless junk (cookies, policy, newsletter, sign up).
4. DO NOT remove competitor pages even if they include “alternatives”.
5. Convert into clean bullet points.
6. NO hallucination.
7. If SERPER data is weak, still infer best-known facts from public knowledge.

STRICT FORMATS:

If section = competitors:
- List top competitors with 1-line explanation each.

If section = financials:
- Revenue
- Profit
- Growth %
- Key business units

If section = risks:
- Top 5 risks with 1-line explanation

If section = opportunities:
- 4–6 opportunities with brief reason

If section = overview:
- Summary
- Business model
- Key products
- Recent updates
"""


class Researcher:

    def run_task(self, company, task):
        section = task["section"]

        # Better SERPER queries
        if section == "competitors":
            query = f"{company} competitors rivals market share 2024 2025 analysis"
        else:
            query = f"{company} {section} 2024 2025 analysis factual data"

        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {"q": query}

        # ---- SERPER CALL ----
        try:
            r = requests.post(SEARCH_URL, json=payload, headers=headers, timeout=10)
            data = r.json()
        except:
            data = {"organic": [], "peopleAlsoAsk": []}

        # ---- COLLECT TEXT ----
        lines = []

        for item in data.get("organic", []):
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            lines.append(f"{title} {snippet}")

        for item in data.get("peopleAlsoAsk", []):
            q = item.get("question", "")
            s = item.get("snippet", "")
            lines.append(f"{q} {s}")

        raw_text = "\n".join(lines)

        # ---- SMART FILTERING ----
        clean_lines = []
        for line in raw_text.split("\n"):
            L = line.lower()

            # Remove ONLY true junk
            if any(bad in L for bad in [
                "cookie", "privacy", "terms", "subscribe",
                "sign up", "newsletter", "template"
            ]):
                continue

            clean_lines.append(line)

        cleaned_text = "\n".join([x for x in clean_lines if x.strip()])

        # If the cleaned text is EMPTY → use raw data instead
        if cleaned_text.strip() == "":
            cleaned_text = raw_text

        # If still empty → force GPT to infer
        if cleaned_text.strip() == "":
            cleaned_text = f"No SERPER data. Give best possible {section} for {company}."

        # ---- GPT PROCESSING ----
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Company: {company}\nSection: {section}\n\nRaw Data:\n{cleaned_text}"
                    }
                ],
                max_tokens=600
            )

            result = resp.choices[0].message.content.strip()

            return {
                "company": company,
                "section": section,
                "raw_records": result.split("\n")
            }

        except Exception:
            return {
                "company": company,
                "section": section,
                "raw_records": ["Not enough reliable data found."]
            }

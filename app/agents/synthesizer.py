from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are the SYNTHESIZER — a senior corporate analyst.

Your job:
1. Combine multiple section summaries (competitors, financials, risks, etc.)
2. Remove repetition.
3. Keep writing clean, factual, high-quality.
4. Use executive tone — brief but strong.
5. Structure the final report as:

### Company Overview
- ...

### Competitors
- ...

### Financials
- ...

### Opportunities
- ...

### Risks
- ...

### Final Takeaway
- ...

6. If any section is missing, skip it naturally.
7. No hallucination.
"""


class Synthesizer:

    def merge_sections(self, company, section_summaries: dict):
        """
        section_summaries = {
            "overview": "...",
            "competitors": "...",
            "risks": "...",
            ...
        }
        """

        if not section_summaries:
            return "No summaries available to synthesize."

        # Turn dict into structured text
        formatted = []
        for sec, content in section_summaries.items():
            formatted.append(f"### {sec.capitalize()}\n{content}")

        all_text = "\n\n".join(formatted)

        # Ask GPT to synthesize
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Synthesize a final enterprise report for {company}.\n\n{all_text}"
                    }
                ],
                max_tokens=600
            )

            return response.choices[0].message.content.strip()

        except Exception:
            # fallback
            return all_text

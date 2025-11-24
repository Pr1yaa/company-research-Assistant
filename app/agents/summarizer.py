import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- HARD FALLBACK FACTS ----------
FALLBACK_DATA = {
    "competitors": {
        "google": [
            "Microsoft – Bing search + Azure AI ecosystem",
            "Amazon – AWS cloud + advertising competition",
            "Meta – Online ads + LLaMA AI models",
            "Apple – AI ecosystem + devices",
            "OpenAI – ChatGPT + search disruption"
        ],
        "amazon": [
            "Walmart – Retail and logistics competition",
            "Microsoft – Azure vs AWS cloud",
            "Google – Cloud and advertising competition",
            "Alibaba – E-commerce + cloud",
            "Target – US retail competition"
        ]
    },
    "financials": {
        "google": [
            "Revenue: Strong growth led by Search & Cloud.",
            "Profit: Healthy operating margins (25–30%).",
            "Growth: Cloud fastest-growing segment.",
            "Units: Google Search, YouTube, Cloud, Android, Hardware."
        ],
        "amazon": [
            "Revenue: Driven by e-commerce & AWS.",
            "Profit: AWS contributes majority of profit.",
            "Growth: Strong cloud growth; retail softer.",
            "Units: AWS, Marketplace, Prime, Logistics."
        ]
    },
    "overview": {
        "google": [
            "Alphabet’s core business is search & digital ads.",
            "Major products: Google Search, YouTube, Chrome, Android.",
            "Emerging: Cloud, AI (Gemini), hardware.",
            "Recent: Focus on AI unification across products."
        ]
    }
}


class Summarizer:

    def summarize_section(self, section, records):

        # Clean incoming records
        cleaned_records = [str(r).strip() for r in records if r.strip()]

        # Extract company if available (fallback: google)
        company_name = "google"
        try:
            first_line = cleaned_records[0].lower()
            for known in ["google", "amazon", "tesla", "microsoft", "meta", "apple"]:
                if known in first_line:
                    company_name = known
                    break
        except:
            pass

        # ---------- HARD FALLBACK TRIGGER ----------
        no_data = (
            len(cleaned_records) == 0 or
            cleaned_records == ["Not enough reliable data found."] or
            all("not enough" in r.lower() for r in cleaned_records)
        )

        if no_data:
            return self._fallback(section, company_name)

        # ---------- GPT SUMMARIZATION ----------
        raw_text = "\n".join(cleaned_records)

        TEMPLATE = f"""
You are a senior business analyst.

Rewrite the following verified lines into clean bullet points.

Rules:
- 4 to 8 bullets.
- Executive, concise, fact-oriented.
- No paragraphs.
- No hallucination.
- Fix incomplete sentences.
- Use strong bullet structure.

Section: {section}

Text:
{raw_text}
"""

        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": TEMPLATE}],
                max_tokens=400
            )

            return resp.choices[0].message.content.strip()

        except:
            # minimal fallback
            return self._fallback(section, company_name)

    # ------------------------------------------------
    # FALLBACK LOGIC
    # ------------------------------------------------
    def _fallback(self, section, company):
        sec = section.lower()
        comp = company.lower()

        bullets = FALLBACK_DATA.get(sec, {}).get(comp, None)

        if bullets:
            return "\n".join(f"• {b}" for b in bullets)

        # default message
        return "• No reliable data available."

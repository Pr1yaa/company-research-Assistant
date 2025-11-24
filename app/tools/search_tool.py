import os
import requests

class SearchTool:
    """
    Small wrapper for Serper.dev Google Search API.
    Expects SERPER_API_KEY in environment.
    Returns a clean snippet and url.
    """

    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")

    def search(self, query: str):
        if not self.api_key:
            return None

        url = "https://google.serper.dev/search"
        payload = {"q": query}
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=12)
            if resp.status_code != 200:
                return None

            data = resp.json()

            # best organic result
            organic = data.get("organic", [])
            if organic:
                best = organic[0]
                return {
                    "title": best.get("title", ""),
                    "text": best.get("snippet", ""),
                    "url": best.get("link", "")
                }

            # fallback: knowledge graph or answer box
            kb = data.get("knowledgeGraph") or data.get("answerBox")
            if kb:
                text = kb.get("description") or kb.get("snippet") or ""
                return {"title": "", "text": text, "url": ""}

            return None

        except:
            return None

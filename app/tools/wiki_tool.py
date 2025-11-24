# app/tools/wiki_tool.py

import wikipedia

class WikiTool:
    """
    Improved Wikipedia Lookup:
    - Avoids Nikola Tesla confusion
    - Prefers the company page "Tesla, Inc."
    """

    def lookup(self, company: str):
        try:
            # Try exact query first
            try_query = company

            # If someone enters "Tesla", try company explicitly
            if company.lower().strip() == "tesla":
                try_query = "Tesla, Inc."

            page = wikipedia.page(title=try_query, auto_suggest=False)
            return {
                "summary": page.summary[:1000],
                "url": page.url
            }

        except Exception:
            # Fallback: Search for correct page
            try:
                results = wikipedia.search(company)
                if not results:
                    return None

                # Prefer company pages, not people
                for r in results:
                    if "Inc" in r or "company" in r or "Tesla, Inc" in r:
                        page = wikipedia.page(r, auto_suggest=False)
                        return {
                            "summary": page.summary[:1000],
                            "url": page.url
                        }

                # If no company found, just take first result
                page = wikipedia.page(results[0], auto_suggest=False)
                return {
                    "summary": page.summary[:1000],
                    "url": page.url
                }

            except:
                return None

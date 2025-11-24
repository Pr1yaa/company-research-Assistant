# app/tools/finance_tool.py

import yfinance as yf

TICKER_MAP = {
    "tesla": "TSLA",
    "apple": "AAPL",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "microsoft": "MSFT",
    "amazon": "AMZN",
    "meta": "META",
    "facebook": "META",
    "netflix": "NFLX"
}

class FinanceTool:
    """
    Finance API wrapper using yfinance.
    Automatically converts company name → ticker.
    """

    def resolve_ticker(self, company: str):
        cname = company.lower().strip()

        # Step 1: direct dictionary match
        if cname in TICKER_MAP:
            return TICKER_MAP[cname]

        # Step 2: Try using yfinance autocomplete
        try:
            guess = yf.Ticker(company)
            info = guess.info
            if "symbol" in info:
                return info["symbol"]
        except:
            pass

        # Step 3: fallback: return upper-case original
        return company.upper()

    def fetch_financials(self, company: str):
        ticker_symbol = self.resolve_ticker(company)
        ticker = yf.Ticker(ticker_symbol)

        try:
            financials = ticker.financials
            if financials is None or financials.empty:
                return None

            data = {}

            if "Total Revenue" in financials.index:
                data["latest_revenue"] = float(financials.loc["Total Revenue"].iloc[0])

            if "Net Income" in financials.index:
                data["latest_net_income"] = float(financials.loc["Net Income"].iloc[0])

            return data

        except Exception:
            return None

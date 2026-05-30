from datetime import datetime

from app.agents.orchestrator import ResearchOrchestrator
from app.agents.portfolio_advisor import PortfolioAdvisorAgent
from app.providers.market_data import MarketDataProvider
from app.schemas.market import DailyReport, MarketSummary, StockRecommendation


class DailyReportService:
    def __init__(self, market_data: MarketDataProvider, orchestrator: ResearchOrchestrator):
        self.market_data = market_data
        self.orchestrator = orchestrator

    async def generate(self, holdings: list[dict] | None = None) -> DailyReport:
        candidates = ["NVDA", "MSFT", "AAPL", "D05.SI", "O39.SI", "U11.SI", "9CI.SI"]
        reports = [await self.orchestrator.research(ticker) for ticker in candidates]
        recommendations: list[StockRecommendation] = [report.recommendation for report in reports]
        market_finding = reports[0].agent_findings[0]
        indices = [await self.market_data.quote(t) for t in ["^STI", "^GSPC", "^IXIC"]]
        summary = MarketSummary(
            generated_at=datetime.utcnow(),
            indices=indices,
            top_gainers=sorted([await self.market_data.quote(t) for t in candidates[:3]], key=lambda q: q.change_percent, reverse=True),
            top_losers=sorted([await self.market_data.quote(t) for t in candidates[-3:]], key=lambda q: q.change_percent),
            macro_events=["US rate expectations", "SGD liquidity", "Mega-cap technology earnings"],
            ai_summary=market_finding.summary,
        )
        portfolio = await PortfolioAdvisorAgent(self.market_data).summarize(holdings or []) if holdings else None
        return DailyReport(
            report_date=datetime.now().date().isoformat(),
            market_summary=summary,
            top_buy_ideas=[r for r in recommendations if r.action == "BUY"][:5],
            hold_ideas=[r for r in recommendations if r.action == "HOLD"][:5],
            stocks_to_watch=[r.ticker for r in recommendations if r.action != "SELL"][:5],
            sell_alerts=[r for r in recommendations if r.action == "SELL"][:5],
            major_risks_today=[
                "Rate-sensitive valuations could compress if bond yields rise.",
                "Earnings revisions remain the key catalyst for mega-cap technology.",
                "SGX liquidity can amplify price moves in smaller counters.",
            ],
            portfolio_summary=portfolio,
        )

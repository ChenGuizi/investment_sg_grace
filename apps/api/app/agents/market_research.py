from datetime import datetime

from app.agents.base import Agent, ResearchContext
from app.schemas.common import Score
from app.schemas.market import AgentFinding, MarketSummary


class MarketResearchAgent(Agent):
    name = "Market Research Agent"

    async def run(self, context: ResearchContext) -> ResearchContext:
        indices = [await self.market_data.quote(t) for t in ["^STI", "^GSPC", "^IXIC"]]
        gainers = [await self.market_data.quote(t) for t in ["NVDA", "MSFT", "D05.SI"]]
        losers = [await self.market_data.quote(t) for t in ["AAPL", "9CI.SI", "O39.SI"]]
        summary = MarketSummary(
            generated_at=datetime.utcnow(),
            indices=indices,
            top_gainers=sorted(gainers, key=lambda q: q.change_percent, reverse=True),
            top_losers=sorted(losers, key=lambda q: q.change_percent),
            macro_events=[
                "Markets remain sensitive to US rate expectations.",
                "Singapore banks continue to track net interest margin trends.",
                "Earnings guidance is the main near-term catalyst for mega-cap technology.",
            ],
            ai_summary=(
                "Risk appetite is constructive but selective. Momentum remains strongest in profitable "
                "technology and quality financials, while valuation discipline is important after strong rallies."
            ),
        )
        context.artifacts["market_summary"] = summary
        context.findings.append(
            AgentFinding(
                agent=self.name,
                score=Score(value=72, label="Constructive", explanation="Broad indices are stable with selective leadership."),
                summary=summary.ai_summary,
            )
        )
        return context

from app.agents.base import Agent, ResearchContext
from app.schemas.common import Evidence
from app.schemas.market import StockRecommendation


class RecommendationAgent(Agent):
    name = "Recommendation Agent"

    async def run(self, context: ResearchContext) -> ResearchContext:
        scores = {finding.agent: finding.score.value for finding in context.findings}
        fundamental = scores.get("Fundamental Analysis Agent", 50)
        technical = scores.get("Technical Analysis Agent", 50)
        news = scores.get("News Intelligence Agent", 50)
        risk_quality = scores.get("Risk Agent", 50)
        market = scores.get("Market Research Agent", 50)
        combined = fundamental * 0.3 + technical * 0.25 + news * 0.2 + risk_quality * 0.15 + market * 0.1
        action = "BUY" if combined >= 70 else "SELL" if combined <= 42 else "HOLD"
        quote = await self.market_data.quote(context.ticker)
        recommendation = StockRecommendation(
            ticker=context.ticker,
            action=action,
            confidence=round(abs(combined - 50) * 1.2 + 55, 2),
            target_price=round(quote.price * (1.12 if action == "BUY" else 0.92 if action == "SELL" else 1.03), 2),
            reasons=[
                f"Composite agent score is {combined:.1f}/100.",
                f"Fundamental score is {fundamental:.1f}; technical score is {technical:.1f}.",
                f"News sentiment score is {news:.1f}.",
            ],
            risks=context.artifacts.get("risk").factors if context.artifacts.get("risk") else [],
            what_changed=[
                "Latest news flow and technical trend were incorporated into today's recommendation.",
                "Risk score was adjusted for current beta and volatility assumptions.",
            ],
            evidence=[
                Evidence(claim=f"{finding.agent}: {finding.summary}", citations=[c for e in finding.evidence for c in e.citations])
                for finding in context.findings
            ],
        )
        context.artifacts["recommendation"] = recommendation
        return context

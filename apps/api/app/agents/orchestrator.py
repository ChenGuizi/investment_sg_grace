from datetime import datetime

from app.agents.base import ResearchContext
from app.agents.critic import CriticAgent
from app.agents.fundamental_analysis import FundamentalAnalysisAgent
from app.agents.market_research import MarketResearchAgent
from app.agents.news_intelligence import NewsIntelligenceAgent
from app.agents.recommendation import RecommendationAgent
from app.agents.risk import RiskAgent
from app.agents.technical_analysis import TechnicalAnalysisAgent
from app.providers.market_data import MarketDataProvider
from app.providers.news import NewsProvider
from app.schemas.market import DeepResearchReport


class ResearchOrchestrator:
    def __init__(self, market_data: MarketDataProvider, news: NewsProvider):
        self.agents = [
            MarketResearchAgent(market_data, news),
            NewsIntelligenceAgent(market_data, news),
            FundamentalAnalysisAgent(market_data, news),
            TechnicalAnalysisAgent(market_data, news),
            RiskAgent(market_data, news),
            RecommendationAgent(market_data, news),
        ]
        self.critic = CriticAgent()

    async def research(self, ticker: str, user_profile: dict | None = None) -> DeepResearchReport:
        context = ResearchContext(ticker=ticker.upper(), user_profile=user_profile or {})
        for agent in self.agents:
            context = await agent.run(context)
        critic_notes = self.critic.review(context)
        recommendation = context.artifacts["recommendation"]
        citations = [citation for evidence in recommendation.evidence for citation in evidence.citations]
        return DeepResearchReport(
            ticker=context.ticker,
            generated_at=datetime.utcnow(),
            executive_summary=(
                f"{context.ticker} is rated {recommendation.action} with {recommendation.confidence:.0f}% confidence. "
                f"The view combines market context, news, fundamentals, technicals, and risk."
            ),
            investment_thesis="The thesis is based on durable fundamentals, current price momentum, news impact, and risk-adjusted upside.",
            bull_case=recommendation.reasons,
            bear_case=recommendation.risks,
            key_risks=recommendation.risks,
            valuation=f"Target price estimate: {recommendation.target_price}. Valuation is blended from fundamentals and risk-adjusted momentum.",
            recommendation=recommendation,
            agent_findings=context.findings,
            citations=citations,
            critic_notes=critic_notes,
        )

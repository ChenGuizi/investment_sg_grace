import pytest

from app.agents.orchestrator import ResearchOrchestrator
from app.providers.market_data import DemoMarketDataProvider
from app.providers.news import DemoNewsProvider


@pytest.mark.asyncio
async def test_research_report_has_explainable_recommendation():
    orchestrator = ResearchOrchestrator(DemoMarketDataProvider(), DemoNewsProvider())
    report = await orchestrator.research("NVDA")

    assert report.recommendation.action in {"BUY", "HOLD", "SELL"}
    assert report.recommendation.reasons
    assert report.recommendation.risks
    assert report.recommendation.evidence
    assert report.critic_notes

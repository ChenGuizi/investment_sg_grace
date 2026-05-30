import pytest

from app.agents.portfolio_advisor import PortfolioAdvisorAgent
from app.providers.market_data import DemoMarketDataProvider


@pytest.mark.asyncio
async def test_portfolio_summary_calculates_exposure():
    advisor = PortfolioAdvisorAgent(DemoMarketDataProvider())
    summary = await advisor.summarize(
        [
            {"ticker": "NVDA", "quantity": 2, "average_cost": 100},
            {"ticker": "D05.SI", "quantity": 10, "average_cost": 30},
        ]
    )

    assert summary.total_value > 0
    assert summary.holdings
    assert summary.sector_exposure
    assert summary.recommendations

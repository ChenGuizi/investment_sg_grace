from collections import defaultdict

from app.providers.market_data import MarketDataProvider
from app.schemas.market import PortfolioHolding, PortfolioSummary


class PortfolioAdvisorAgent:
    def __init__(self, market_data: MarketDataProvider):
        self.market_data = market_data

    async def summarize(self, holdings: list[dict]) -> PortfolioSummary:
        rows: list[PortfolioHolding] = []
        sector_values: dict[str, float] = defaultdict(float)
        total_value = 0.0
        total_cost = 0.0
        for holding in holdings:
            quote = await self.market_data.quote(holding["ticker"])
            market_value = quote.price * holding["quantity"]
            cost = holding["average_cost"] * holding["quantity"]
            total_value += market_value
            total_cost += cost
            sector_values[quote.sector] += market_value
            rows.append(
                PortfolioHolding(
                    ticker=quote.ticker,
                    quantity=holding["quantity"],
                    average_cost=holding["average_cost"],
                    current_price=quote.price,
                    market_value=round(market_value, 2),
                    unrealized_pl=round(market_value - cost, 2),
                    unrealized_pl_percent=round(((market_value - cost) / cost) * 100, 2) if cost else 0,
                    sector=quote.sector,
                    currency=quote.currency,
                )
            )
        exposure = {sector: round(value / total_value * 100, 2) for sector, value in sector_values.items()} if total_value else {}
        recommendations = []
        for sector, percent in exposure.items():
            if percent > 45:
                recommendations.append(f"Reduce concentration in {sector}; current exposure is {percent:.1f}%.")
        if not recommendations:
            recommendations.append("Portfolio is reasonably diversified across current holdings.")
        pl = total_value - total_cost
        return PortfolioSummary(
            total_value=round(total_value, 2),
            total_pl=round(pl, 2),
            total_pl_percent=round((pl / total_cost) * 100, 2) if total_cost else 0,
            holdings=rows,
            sector_exposure=exposure,
            recommendations=recommendations,
            risk_level="High" if any(v > 55 for v in exposure.values()) else "Medium",
        )

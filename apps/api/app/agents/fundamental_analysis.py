from app.agents.base import Agent, ResearchContext
from app.schemas.common import Evidence, Score
from app.schemas.market import AgentFinding


class FundamentalAnalysisAgent(Agent):
    name = "Fundamental Analysis Agent"

    async def run(self, context: ResearchContext) -> ResearchContext:
        metrics = await self.market_data.fundamentals(context.ticker)
        growth = min((metrics.revenue_growth + metrics.eps_growth) * 160, 35)
        profitability = min((metrics.operating_margin + metrics.roe + metrics.roic) * 70, 35)
        valuation = max(0, 30 - max(metrics.forward_pe - 18, 0) * 0.9 - max(metrics.peg - 1.8, 0) * 5)
        score = round(growth + profitability + valuation, 2)
        context.artifacts["fundamentals"] = metrics
        context.findings.append(
            AgentFinding(
                agent=self.name,
                score=Score(
                    value=min(score, 100),
                    label="Strong" if score >= 75 else "Fair" if score >= 55 else "Weak",
                    explanation="Combines growth, profitability, leverage, and valuation metrics.",
                ),
                summary=(
                    f"Revenue growth {metrics.revenue_growth:.1%}, EPS growth {metrics.eps_growth:.1%}, "
                    f"forward PE {metrics.forward_pe:.1f}, ROE {metrics.roe:.1%}."
                ),
                evidence=[
                    Evidence(claim="Fundamental score reflects growth quality adjusted for valuation."),
                ],
            )
        )
        return context

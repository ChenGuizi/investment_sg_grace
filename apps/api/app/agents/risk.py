from app.agents.base import Agent, ResearchContext
from app.schemas.common import Evidence, Score
from app.schemas.market import AgentFinding, RiskAssessment


class RiskAgent(Agent):
    name = "Risk Agent"

    async def run(self, context: ResearchContext) -> ResearchContext:
        ticker_seed = sum(ord(c) for c in context.ticker)
        beta = round(0.7 + (ticker_seed % 90) / 100, 2)
        volatility = round(0.18 + (ticker_seed % 35) / 100, 2)
        score = min(100, round(beta * 24 + volatility * 75, 2))
        level = "High" if score >= 65 else "Medium" if score >= 38 else "Low"
        factors = [
            "Earnings surprise risk around upcoming reporting windows.",
            "Valuation sensitivity to interest-rate expectations.",
        ]
        if context.ticker.endswith(".SI"):
            factors.append("Singapore market liquidity and currency exposure.")
        assessment = RiskAssessment(
            ticker=context.ticker,
            level=level,
            score=score,
            volatility=volatility,
            beta=beta,
            factors=factors,
        )
        context.artifacts["risk"] = assessment
        context.findings.append(
            AgentFinding(
                agent=self.name,
                score=Score(value=100 - score, label=level, explanation="Higher volatility and beta reduce risk quality."),
                summary=f"Risk is {level.lower()} with beta {beta} and volatility {volatility:.1%}.",
                evidence=[Evidence(claim=f"Primary risks: {'; '.join(factors)}")],
            )
        )
        return context

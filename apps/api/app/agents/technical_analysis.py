from app.agents.base import Agent, ResearchContext
from app.schemas.common import Evidence, Score
from app.schemas.market import AgentFinding


class TechnicalAnalysisAgent(Agent):
    name = "Technical Analysis Agent"

    async def run(self, context: ResearchContext) -> ResearchContext:
        metrics = await self.market_data.technicals(context.ticker)
        trend_score = 35 if metrics.trend == "Uptrend" else 22 if metrics.trend == "Sideways" else 10
        rsi_score = 25 if 45 <= metrics.rsi <= 68 else 16 if metrics.rsi < 75 else 8
        ma_score = 30 if metrics.sma20 > metrics.sma50 > metrics.sma200 else 20 if metrics.sma50 > metrics.sma200 else 8
        macd_score = 10 if metrics.macd > 0 else 3
        score = trend_score + rsi_score + ma_score + macd_score
        context.artifacts["technicals"] = metrics
        context.findings.append(
            AgentFinding(
                agent=self.name,
                score=Score(
                    value=score,
                    label="Bullish" if score >= 70 else "Neutral" if score >= 45 else "Bearish",
                    explanation="Evaluates trend, RSI, MACD, and moving average alignment.",
                ),
                summary=f"{context.ticker} is in a {metrics.trend.lower()} with RSI {metrics.rsi:.1f}.",
                evidence=[
                    Evidence(
                        claim=(
                            f"Support near {metrics.support}, resistance near {metrics.resistance}, "
                            f"SMA50 {metrics.sma50}, SMA200 {metrics.sma200}."
                        )
                    )
                ],
            )
        )
        return context

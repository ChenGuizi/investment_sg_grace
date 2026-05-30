from app.agents.base import Agent, ResearchContext
from app.schemas.common import Citation, Evidence, Score
from app.schemas.market import AgentFinding


class NewsIntelligenceAgent(Agent):
    name = "News Intelligence Agent"

    async def run(self, context: ResearchContext) -> ResearchContext:
        articles = await self.news.articles(context.ticker, limit=10)
        unique = {article.headline.lower(): article for article in articles}
        ranked = sorted(unique.values(), key=lambda a: a.importance, reverse=True)
        sentiment = sum(a.sentiment_score * a.importance for a in ranked) / max(sum(a.importance for a in ranked), 1)
        score = round((sentiment + 1) * 50, 2)
        context.artifacts["news"] = ranked
        context.findings.append(
            AgentFinding(
                agent=self.name,
                score=Score(
                    value=score,
                    label="Bullish" if score >= 65 else "Bearish" if score <= 40 else "Mixed",
                    explanation="Weighted sentiment across deduplicated high-importance articles.",
                ),
                summary=f"{context.ticker} news flow is {('positive' if score >= 65 else 'mixed' if score > 40 else 'negative')}.",
                evidence=[
                    Evidence(
                        claim=article.summary,
                        citations=[
                            Citation(
                                title=article.headline,
                                url=article.url,
                                publisher=article.publisher,
                                published_at=article.published_at,
                            )
                        ],
                    )
                    for article in ranked[:3]
                ],
            )
        )
        return context

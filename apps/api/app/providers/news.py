from datetime import datetime, timedelta
from uuid import uuid5, NAMESPACE_URL

from app.schemas.market import NewsArticle


class NewsProvider:
    async def articles(self, ticker: str | None = None, limit: int = 10) -> list[NewsArticle]:
        raise NotImplementedError


class DemoNewsProvider(NewsProvider):
    async def articles(self, ticker: str | None = None, limit: int = 10) -> list[NewsArticle]:
        subject = ticker.upper() if ticker else "global markets"
        templates = [
            (
                f"{subject} investors watch earnings revisions as rates remain in focus",
                "Analysts are reassessing growth expectations as macro data and earnings guidance shift.",
                "Reuters Demo",
                "Neutral",
                0.08,
                72,
            ),
            (
                f"{subject} sees positive demand signals from enterprise spending",
                "Recent commentary points to resilient demand and improving order visibility.",
                "CNBC Demo",
                "Positive",
                0.54,
                86,
            ),
            (
                f"Valuation concerns temper enthusiasm around {subject}",
                "Portfolio managers cite elevated multiples and sensitivity to rate expectations.",
                "Financial Times Demo",
                "Negative",
                -0.31,
                68,
            ),
        ]
        articles: list[NewsArticle] = []
        for idx, item in enumerate(templates[:limit]):
            headline, summary, publisher, impact, sentiment, importance = item
            url = f"https://example.com/news/{ticker or 'market'}/{idx}"
            articles.append(
                NewsArticle(
                    id=str(uuid5(NAMESPACE_URL, url)),
                    ticker=ticker,
                    headline=headline,
                    summary=summary,
                    publisher=publisher,
                    url=url,
                    published_at=datetime.utcnow() - timedelta(hours=idx + 1),
                    impact=impact,
                    sentiment_score=sentiment,
                    importance=importance,
                )
            )
        return articles


def get_news_provider() -> NewsProvider:
    return DemoNewsProvider()

from app.providers.news import NewsProvider
from app.providers.vector_store import VectorDocument, VectorStore


class NewsIngestionService:
    def __init__(self, news_provider: NewsProvider, vector_store: VectorStore):
        self.news_provider = news_provider
        self.vector_store = vector_store

    async def ingest_ticker_news(self, ticker: str) -> int:
        articles = await self.news_provider.articles(ticker, limit=20)
        documents = [
            VectorDocument(
                id=article.id,
                text=f"{article.headline}\n{article.summary}",
                metadata={
                    "ticker": ticker,
                    "publisher": article.publisher,
                    "url": article.url,
                    "published_at": article.published_at.isoformat(),
                    "impact": article.impact,
                },
            )
            for article in articles
        ]
        await self.vector_store.upsert(documents)
        return len(documents)

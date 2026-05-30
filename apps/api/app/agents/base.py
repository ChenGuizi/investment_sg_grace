from dataclasses import dataclass, field

from app.providers.market_data import MarketDataProvider
from app.providers.news import NewsProvider
from app.schemas.market import AgentFinding


@dataclass
class ResearchContext:
    ticker: str
    user_profile: dict = field(default_factory=dict)
    findings: list[AgentFinding] = field(default_factory=list)
    artifacts: dict = field(default_factory=dict)


class Agent:
    name = "agent"

    def __init__(self, market_data: MarketDataProvider, news: NewsProvider):
        self.market_data = market_data
        self.news = news

    async def run(self, context: ResearchContext) -> ResearchContext:
        raise NotImplementedError

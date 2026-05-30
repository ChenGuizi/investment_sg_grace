from app.agents.orchestrator import ResearchOrchestrator
from app.core.config import Settings, get_settings
from app.providers.market_data import MarketDataProvider, get_market_data_provider
from app.providers.news import NewsProvider, get_news_provider


def settings_dep() -> Settings:
    return get_settings()


def market_data_dep() -> MarketDataProvider:
    return get_market_data_provider()


def news_dep() -> NewsProvider:
    return get_news_provider()


def orchestrator_dep() -> ResearchOrchestrator:
    return ResearchOrchestrator(get_market_data_provider(), get_news_provider())

from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.agents.orchestrator import ResearchOrchestrator
from app.agents.portfolio_advisor import PortfolioAdvisorAgent
from app.api.deps import market_data_dep, orchestrator_dep, settings_dep
from app.core.config import Settings
from app.providers.market_data import MarketDataProvider
from app.providers.news import get_news_provider
from app.providers.vector_store import get_vector_store
from app.schemas.market import DailyReport, DeepResearchReport, MarketSummary, PortfolioSummary
from app.services.email import EmailService
from app.services.ingestion import NewsIngestionService
from app.services.knowledge_graph import KnowledgeGraphBuilder
from app.services.reporting import DailyReportService

router = APIRouter()


class HoldingInput(BaseModel):
    ticker: str
    quantity: float
    average_cost: float


class PortfolioRequest(BaseModel):
    holdings: list[HoldingInput]


class EmailReportRequest(BaseModel):
    recipient: str
    holdings: list[HoldingInput] = []


@router.get("/health")
async def health() -> dict:
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@router.get("/monitoring/readiness")
async def readiness() -> dict:
    return {
        "status": "ready",
        "checks": {
            "api": "ok",
            "scheduler": "configured",
            "market_data_provider": "demo",
            "news_provider": "demo",
        },
    }


@router.get("/market/summary", response_model=MarketSummary)
async def market_summary(market_data: MarketDataProvider = Depends(market_data_dep)) -> MarketSummary:
    indices = [await market_data.quote(t) for t in ["^STI", "^GSPC", "^IXIC"]]
    gainers = [await market_data.quote(t) for t in ["NVDA", "MSFT", "D05.SI"]]
    losers = [await market_data.quote(t) for t in ["AAPL", "9CI.SI", "O39.SI"]]
    return MarketSummary(
        generated_at=datetime.utcnow(),
        indices=indices,
        top_gainers=sorted(gainers, key=lambda q: q.change_percent, reverse=True),
        top_losers=sorted(losers, key=lambda q: q.change_percent),
        macro_events=[
            "US rate expectations remain the dominant global equity driver.",
            "Singapore bank earnings are sensitive to net interest margin trends.",
            "AI infrastructure spending continues to shape semiconductor leadership.",
        ],
        ai_summary="Markets are constructive but selective. Quality growth and cash-generative Singapore financials screen well, while valuation risk deserves active monitoring.",
    )


@router.get("/stocks/{ticker}/quote")
async def quote(ticker: str, market_data: MarketDataProvider = Depends(market_data_dep)):
    return await market_data.quote(ticker)


@router.get("/stocks/{ticker}/prices")
async def prices(ticker: str, days: int = 260, market_data: MarketDataProvider = Depends(market_data_dep)):
    return await market_data.prices(ticker, days=days)


@router.get("/stocks/{ticker}/news")
async def news(ticker: str):
    return await get_news_provider().articles(ticker, limit=10)


@router.get("/stocks/{ticker}/fundamentals")
async def fundamentals(ticker: str, market_data: MarketDataProvider = Depends(market_data_dep)):
    return await market_data.fundamentals(ticker)


@router.get("/stocks/{ticker}/technicals")
async def technicals(ticker: str, market_data: MarketDataProvider = Depends(market_data_dep)):
    return await market_data.technicals(ticker)


@router.get("/research/{ticker}", response_model=DeepResearchReport)
async def research(ticker: str, orchestrator: ResearchOrchestrator = Depends(orchestrator_dep)) -> DeepResearchReport:
    return await orchestrator.research(ticker)


@router.get("/research/{ticker}/knowledge-graph")
async def knowledge_graph(ticker: str, orchestrator: ResearchOrchestrator = Depends(orchestrator_dep)):
    report = await orchestrator.research(ticker)
    return KnowledgeGraphBuilder().from_report(report)


@router.post("/research/{ticker}/ingest-news")
async def ingest_news(ticker: str):
    count = await NewsIngestionService(get_news_provider(), get_vector_store()).ingest_ticker_news(ticker)
    return {"ticker": ticker.upper(), "documents_indexed": count}


@router.post("/portfolio/summary", response_model=PortfolioSummary)
async def portfolio_summary(payload: PortfolioRequest, market_data: MarketDataProvider = Depends(market_data_dep)) -> PortfolioSummary:
    advisor = PortfolioAdvisorAgent(market_data)
    return await advisor.summarize([holding.model_dump() for holding in payload.holdings])


@router.post("/reports/daily", response_model=DailyReport)
async def daily_report(
    payload: PortfolioRequest,
    market_data: MarketDataProvider = Depends(market_data_dep),
    orchestrator: ResearchOrchestrator = Depends(orchestrator_dep),
) -> DailyReport:
    service = DailyReportService(market_data, orchestrator)
    return await service.generate([holding.model_dump() for holding in payload.holdings])


@router.post("/reports/daily/email")
async def email_daily_report(
    payload: EmailReportRequest,
    settings: Settings = Depends(settings_dep),
    market_data: MarketDataProvider = Depends(market_data_dep),
    orchestrator: ResearchOrchestrator = Depends(orchestrator_dep),
):
    report = await DailyReportService(market_data, orchestrator).generate([holding.model_dump() for holding in payload.holdings])
    return await EmailService(settings).send_daily_report(payload.recipient, report)

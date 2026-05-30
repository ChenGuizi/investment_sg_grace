from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import Citation, Evidence, Impact, Market, Recommendation, RiskLevel, Score


class PricePoint(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class StockQuote(BaseModel):
    ticker: str
    name: str
    market: Market
    currency: str
    price: float
    change: float
    change_percent: float
    sector: str
    updated_at: datetime


class NewsArticle(BaseModel):
    id: str
    ticker: str | None = None
    headline: str
    summary: str
    publisher: str
    url: str
    published_at: datetime
    impact: Impact = "Neutral"
    sentiment_score: float = Field(ge=-1, le=1, default=0)
    importance: float = Field(ge=0, le=100, default=50)


class MarketSummary(BaseModel):
    generated_at: datetime
    indices: list[StockQuote]
    top_gainers: list[StockQuote]
    top_losers: list[StockQuote]
    macro_events: list[str]
    ai_summary: str
    citations: list[Citation] = Field(default_factory=list)


class FundamentalMetrics(BaseModel):
    ticker: str
    revenue_growth: float
    eps_growth: float
    operating_margin: float
    free_cash_flow_yield: float
    roe: float
    roic: float
    debt_to_equity: float
    pe: float
    forward_pe: float
    peg: float
    price_to_book: float
    ev_to_ebitda: float


class TechnicalMetrics(BaseModel):
    ticker: str
    trend: str
    support: float
    resistance: float
    rsi: float
    macd: float
    sma20: float
    sma50: float
    sma200: float
    ema20: float


class RiskAssessment(BaseModel):
    ticker: str
    level: RiskLevel
    score: float = Field(ge=0, le=100)
    volatility: float
    beta: float
    factors: list[str]


class AgentFinding(BaseModel):
    agent: str
    score: Score
    summary: str
    evidence: list[Evidence] = Field(default_factory=list)


class StockRecommendation(BaseModel):
    ticker: str
    action: Recommendation
    confidence: float = Field(ge=0, le=100)
    target_price: float | None = None
    reasons: list[str]
    risks: list[str]
    what_changed: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)


class DeepResearchReport(BaseModel):
    ticker: str
    generated_at: datetime
    executive_summary: str
    investment_thesis: str
    bull_case: list[str]
    bear_case: list[str]
    key_risks: list[str]
    valuation: str
    recommendation: StockRecommendation
    agent_findings: list[AgentFinding]
    citations: list[Citation]
    critic_notes: list[str]


class PortfolioHolding(BaseModel):
    ticker: str
    quantity: float
    average_cost: float
    current_price: float
    market_value: float
    unrealized_pl: float
    unrealized_pl_percent: float
    sector: str
    currency: str


class PortfolioSummary(BaseModel):
    total_value: float
    total_pl: float
    total_pl_percent: float
    holdings: list[PortfolioHolding]
    sector_exposure: dict[str, float]
    recommendations: list[str]
    risk_level: RiskLevel


class DailyReport(BaseModel):
    report_date: str
    market_summary: MarketSummary
    top_buy_ideas: list[StockRecommendation]
    hold_ideas: list[StockRecommendation]
    stocks_to_watch: list[str]
    sell_alerts: list[StockRecommendation]
    major_risks_today: list[str]
    portfolio_summary: PortfolioSummary | None = None

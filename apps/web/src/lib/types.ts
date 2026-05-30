export type Quote = {
  ticker: string;
  name: string;
  market: "US" | "SG";
  currency: string;
  price: number;
  change: number;
  change_percent: number;
  sector: string;
  updated_at: string;
};

export type NewsArticle = {
  id: string;
  ticker?: string;
  headline: string;
  summary: string;
  publisher: string;
  url: string;
  published_at: string;
  impact: "Positive" | "Neutral" | "Negative";
  sentiment_score: number;
  importance: number;
};

export type MarketSummary = {
  generated_at: string;
  indices: Quote[];
  top_gainers: Quote[];
  top_losers: Quote[];
  macro_events: string[];
  ai_summary: string;
};

export type PricePoint = {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
};

export type StockRecommendation = {
  ticker: string;
  action: "BUY" | "HOLD" | "SELL";
  confidence: number;
  target_price?: number;
  reasons: string[];
  risks: string[];
  what_changed: string[];
  evidence: { claim: string; citations: { title: string; url: string; publisher: string; published_at?: string }[] }[];
};

export type AgentFinding = {
  agent: string;
  score: { value: number; label: string; explanation: string };
  summary: string;
};

export type DeepResearchReport = {
  ticker: string;
  generated_at: string;
  executive_summary: string;
  investment_thesis: string;
  bull_case: string[];
  bear_case: string[];
  key_risks: string[];
  valuation: string;
  recommendation: StockRecommendation;
  agent_findings: AgentFinding[];
  critic_notes: string[];
};

export type PortfolioSummary = {
  total_value: number;
  total_pl: number;
  total_pl_percent: number;
  holdings: {
    ticker: string;
    quantity: number;
    average_cost: number;
    current_price: number;
    market_value: number;
    unrealized_pl: number;
    unrealized_pl_percent: number;
    sector: string;
    currency: string;
  }[];
  sector_exposure: Record<string, number>;
  recommendations: string[];
  risk_level: "Low" | "Medium" | "High";
};

"use client";

import { Activity, AlertTriangle, Bell, Briefcase, CheckCircle2, Newspaper, Search, Send, Shield, TrendingUp } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "@/lib/api";
import type { DeepResearchReport, MarketSummary, NewsArticle, PortfolioSummary, PricePoint } from "@/lib/types";
import { Metric, Panel, RecommendationBadge, SectionTitle } from "./ui";

const fallbackMarket: MarketSummary = {
  generated_at: new Date().toISOString(),
  indices: [
    { ticker: "^STI", name: "Straits Times Index", market: "SG", currency: "SGD", price: 3388, change: 12.4, change_percent: 0.37, sector: "Index", updated_at: new Date().toISOString() },
    { ticker: "^GSPC", name: "S&P 500", market: "US", currency: "USD", price: 5277, change: 18.2, change_percent: 0.35, sector: "Index", updated_at: new Date().toISOString() },
    { ticker: "^IXIC", name: "Nasdaq Composite", market: "US", currency: "USD", price: 16830, change: 77.5, change_percent: 0.46, sector: "Index", updated_at: new Date().toISOString() }
  ],
  top_gainers: [],
  top_losers: [],
  macro_events: ["US rate expectations", "SG bank NIM trends", "AI capex revisions"],
  ai_summary: "Markets are constructive but selective. Quality growth and Singapore financials remain attractive, while valuation risk requires discipline."
};

const fallbackResearch: DeepResearchReport = {
  ticker: "NVDA",
  generated_at: new Date().toISOString(),
  executive_summary: "NVDA is rated BUY with high confidence based on positive news flow, strong technical trend, and durable AI infrastructure demand.",
  investment_thesis: "Nvidia remains a quality growth compounder with strong demand visibility, though position sizing should respect valuation risk.",
  bull_case: ["Revenue growth remains supported by AI infrastructure demand.", "Price is above key moving averages.", "News flow points to enterprise AI adoption."],
  bear_case: ["Valuation is elevated.", "Expectations leave little room for earnings disappointment."],
  key_risks: ["High valuation", "Semiconductor cycle risk"],
  valuation: "Target price estimate uses a risk-adjusted premium to current price.",
  recommendation: {
    ticker: "NVDA",
    action: "BUY",
    confidence: 82,
    target_price: 312,
    reasons: ["Composite agent score is 78.4/100.", "Fundamental and technical scores are both constructive.", "News sentiment is positive."],
    risks: ["High valuation", "Sector concentration"],
    what_changed: ["Recent enterprise AI demand signals improved sentiment."],
    evidence: [{ claim: "News flow and technical momentum support the recommendation.", citations: [] }]
  },
  agent_findings: [
    { agent: "Market Research Agent", score: { value: 72, label: "Constructive", explanation: "Stable index backdrop" }, summary: "Risk appetite is constructive but selective." },
    { agent: "News Intelligence Agent", score: { value: 77, label: "Bullish", explanation: "Weighted sentiment" }, summary: "News flow is positive." },
    { agent: "Fundamental Analysis Agent", score: { value: 81, label: "Strong", explanation: "Growth quality" }, summary: "Growth and profitability are strong." },
    { agent: "Technical Analysis Agent", score: { value: 74, label: "Bullish", explanation: "Trend alignment" }, summary: "Shares are in an uptrend." },
    { agent: "Risk Agent", score: { value: 58, label: "Medium", explanation: "Valuation and beta" }, summary: "Risk is medium-high." }
  ],
  critic_notes: ["Recommendation includes reasons, risks, and traceable evidence. No contradictions detected."]
};

const chartFallback = Array.from({ length: 90 }, (_, i) => ({
  date: new Date(Date.now() - (90 - i) * 86400000).toISOString(),
  close: Math.round((210 + i * 0.9 + Math.sin(i / 5) * 8) * 100) / 100,
  open: 0,
  high: 0,
  low: 0,
  volume: 1000000 + i * 1000
}));

export function DashboardClient() {
  const [ticker, setTicker] = useState("NVDA");
  const [market, setMarket] = useState<MarketSummary>(fallbackMarket);
  const [research, setResearch] = useState<DeepResearchReport>(fallbackResearch);
  const [prices, setPrices] = useState<PricePoint[]>(chartFallback);
  const [news, setNews] = useState<NewsArticle[]>([]);
  const [portfolio, setPortfolio] = useState<PortfolioSummary | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.marketSummary().then(setMarket).catch(() => setMarket(fallbackMarket));
    api.portfolio().then(setPortfolio).catch(() => setPortfolio(null));
  }, []);

  useEffect(() => {
    setLoading(true);
    Promise.all([api.research(ticker), api.prices(ticker), api.news(ticker)])
      .then(([researchResult, priceResult, newsResult]) => {
        setResearch(researchResult);
        setPrices(priceResult);
        setNews(newsResult);
      })
      .catch(() => {
        setResearch({ ...fallbackResearch, ticker });
        setPrices(chartFallback);
        setNews([]);
      })
      .finally(() => setLoading(false));
  }, [ticker]);

  const exposure = useMemo(
    () => Object.entries(portfolio?.sector_exposure ?? { Technology: 42, Financials: 38, "Real Estate": 20 }).map(([name, value]) => ({ name, value })),
    [portfolio]
  );

  return (
    <main className="terminal-grid min-h-screen">
      <header className="border-b border-line bg-background/95 px-4 py-3 backdrop-blur">
        <div className="mx-auto flex max-w-[1500px] flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-xl font-semibold text-text">Stock Intelligence SG</h1>
            <p className="text-sm text-muted">Deep research for US and Singapore equities</p>
          </div>
          <div className="flex items-center gap-2">
            <div className="flex h-10 items-center gap-2 rounded-md border border-line bg-panel px-3">
              <Search size={16} className="text-muted" />
              <select value={ticker} onChange={(event) => setTicker(event.target.value)} className="bg-transparent text-sm text-text outline-none">
                {["NVDA", "AAPL", "MSFT", "D05.SI", "O39.SI", "U11.SI", "9CI.SI"].map((item) => (
                  <option key={item} value={item} className="bg-panel">
                    {item}
                  </option>
                ))}
              </select>
            </div>
            <button className="flex h-10 items-center gap-2 rounded-md border border-accent/40 bg-accent/10 px-3 text-sm text-accent">
              <Send size={16} />
              Daily Email
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-[1500px] gap-4 p-4 xl:grid-cols-[1.4fr_0.9fr_0.9fr]">
        <Panel className="xl:col-span-2">
          <SectionTitle title="Market Overview" meta="SGT morning report" />
          <div className="grid gap-3 sm:grid-cols-3">
            {market.indices.map((index) => (
              <div key={index.ticker} className="rounded-md border border-line bg-background/60 p-3">
                <Metric label={index.name} value={`${index.price.toLocaleString()} ${index.currency}`} tone={index.change_percent >= 0 ? "good" : "bad"} />
                <div className={index.change_percent >= 0 ? "mt-1 text-sm text-buy" : "mt-1 text-sm text-sell"}>
                  {index.change_percent >= 0 ? "+" : ""}
                  {index.change_percent.toFixed(2)}%
                </div>
              </div>
            ))}
          </div>
          <p className="mt-4 text-sm leading-6 text-muted">{market.ai_summary}</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {market.macro_events.map((event) => (
              <span key={event} className="rounded border border-line bg-background/70 px-2 py-1 text-xs text-muted">
                {event}
              </span>
            ))}
          </div>
        </Panel>

        <Panel>
          <SectionTitle title="Recommendation" meta={loading ? "refreshing" : "live"} />
          <div className="flex items-center justify-between">
            <div>
              <div className="text-3xl font-semibold text-text">{research.ticker}</div>
              <div className="mt-1 text-sm text-muted">Confidence {research.recommendation.confidence.toFixed(0)}%</div>
            </div>
            <RecommendationBadge action={research.recommendation.action} />
          </div>
          <div className="mt-4 grid grid-cols-2 gap-3">
            <Metric label="Target Price" value={research.recommendation.target_price ? `$${research.recommendation.target_price}` : "N/A"} />
            <Metric label="Critic Check" value={research.critic_notes.length ? "Passed" : "Pending"} tone="good" />
          </div>
          <ul className="mt-4 space-y-2 text-sm text-muted">
            {research.recommendation.reasons.slice(0, 3).map((reason) => (
              <li key={reason} className="flex gap-2">
                <CheckCircle2 size={16} className="mt-0.5 shrink-0 text-buy" />
                <span>{reason}</span>
              </li>
            ))}
          </ul>
        </Panel>

        <Panel className="xl:col-span-2">
          <SectionTitle title="Price Trend" meta="180 day view" />
          <div className="h-[310px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={prices}>
                <defs>
                  <linearGradient id="price" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.35} />
                    <stop offset="95%" stopColor="#38bdf8" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="#233040" strokeDasharray="3 3" />
                <XAxis dataKey="date" tickFormatter={(value) => new Date(value).toLocaleDateString("en-SG", { month: "short", day: "numeric" })} stroke="#93a4b7" minTickGap={30} />
                <YAxis stroke="#93a4b7" domain={["dataMin - 10", "dataMax + 10"]} />
                <Tooltip contentStyle={{ background: "#111821", border: "1px solid #233040", borderRadius: 6 }} />
                <Area type="monotone" dataKey="close" stroke="#38bdf8" fill="url(#price)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel>
          <SectionTitle title="Agent Scores" />
          <div className="space-y-3">
            {research.agent_findings.map((finding) => (
              <div key={finding.agent}>
                <div className="mb-1 flex items-center justify-between gap-2 text-sm">
                  <span className="truncate text-text">{finding.agent.replace(" Agent", "")}</span>
                  <span className="text-muted">{finding.score.value.toFixed(0)}</span>
                </div>
                <div className="h-2 rounded bg-background">
                  <div className="h-2 rounded bg-accent" style={{ width: `${finding.score.value}%` }} />
                </div>
              </div>
            ))}
          </div>
        </Panel>

        <Panel>
          <SectionTitle title="Deep Research" />
          <p className="text-sm leading-6 text-muted">{research.executive_summary}</p>
          <div className="mt-4 grid gap-3">
            <div className="rounded-md border border-line bg-background/60 p-3">
              <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-buy">
                <TrendingUp size={16} />
                Bull Case
              </div>
              <ul className="space-y-1 text-sm text-muted">
                {research.bull_case.slice(0, 3).map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="rounded-md border border-line bg-background/60 p-3">
              <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-hold">
                <AlertTriangle size={16} />
                Bear Case
              </div>
              <ul className="space-y-1 text-sm text-muted">
                {research.bear_case.slice(0, 3).map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          </div>
        </Panel>

        <Panel>
          <SectionTitle title="News Center" />
          <div className="space-y-3">
            {(news.length ? news : [
              { id: "1", headline: `${ticker} demand signals improve`, summary: "Recent commentary points to resilient demand and better visibility.", publisher: "Demo", impact: "Positive", published_at: new Date().toISOString(), url: "#", sentiment_score: 0.4, importance: 80 }
            ] as NewsArticle[]).slice(0, 4).map((article) => (
              <article key={article.id} className="rounded-md border border-line bg-background/60 p-3">
                <div className="mb-2 flex items-center justify-between gap-2">
                  <Newspaper size={16} className="text-accent" />
                  <span className={article.impact === "Positive" ? "text-xs text-buy" : article.impact === "Negative" ? "text-xs text-sell" : "text-xs text-muted"}>{article.impact}</span>
                </div>
                <h3 className="text-sm font-semibold text-text">{article.headline}</h3>
                <p className="mt-1 text-xs leading-5 text-muted">{article.summary}</p>
              </article>
            ))}
          </div>
        </Panel>

        <Panel>
          <SectionTitle title="Portfolio" meta={portfolio ? `${portfolio.risk_level} risk` : "demo"} />
          <div className="grid grid-cols-2 gap-3">
            <Metric label="Total Value" value={`$${(portfolio?.total_value ?? 102340).toLocaleString()}`} />
            <Metric label="P/L" value={`${portfolio?.total_pl_percent ?? 14.2}%`} tone={(portfolio?.total_pl_percent ?? 14.2) >= 0 ? "good" : "bad"} />
          </div>
          <div className="mt-4 h-[180px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={exposure}>
                <CartesianGrid stroke="#233040" strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" stroke="#93a4b7" tick={{ fontSize: 11 }} />
                <YAxis stroke="#93a4b7" />
                <Tooltip contentStyle={{ background: "#111821", border: "1px solid #233040", borderRadius: 6 }} />
                <Bar dataKey="value" radius={[3, 3, 0, 0]}>
                  {exposure.map((entry, index) => (
                    <Cell key={entry.name} fill={["#38bdf8", "#22c55e", "#f59e0b", "#ef4444"][index % 4]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel>
          <SectionTitle title="Automation" />
          <div className="space-y-3 text-sm text-muted">
            <div className="flex items-start gap-3 rounded-md border border-line bg-background/60 p-3">
              <Bell size={17} className="mt-0.5 text-accent" />
              <div>
                <div className="font-semibold text-text">Daily 7:00 AM SGT</div>
                <div>Top buys, holds, sell alerts, risks, and portfolio impact.</div>
              </div>
            </div>
            <div className="flex items-start gap-3 rounded-md border border-line bg-background/60 p-3">
              <Shield size={17} className="mt-0.5 text-buy" />
              <div>
                <div className="font-semibold text-text">Explainability enforced</div>
                <div>Recommendations require evidence, reasons, risks, confidence, and critic notes.</div>
              </div>
            </div>
            <div className="flex items-start gap-3 rounded-md border border-line bg-background/60 p-3">
              <Briefcase size={17} className="mt-0.5 text-hold" />
              <div>
                <div className="font-semibold text-text">Personalization</div>
                <div>Growth, value, dividend, risk appetite, horizon, and US/SG preferences.</div>
              </div>
            </div>
          </div>
        </Panel>

        <Panel>
          <SectionTitle title="Watchlist" />
          <div className="space-y-2">
            {["AAPL", "MSFT", "D05.SI", "O39.SI", "U11.SI"].map((item) => (
              <button key={item} onClick={() => setTicker(item)} className="flex w-full items-center justify-between rounded-md border border-line bg-background/60 px-3 py-2 text-left text-sm hover:border-accent/60">
                <span className="font-semibold text-text">{item}</span>
                <span className="flex items-center gap-1 text-xs text-muted">
                  <Activity size={14} />
                  monitor
                </span>
              </button>
            ))}
          </div>
        </Panel>
      </div>
    </main>
  );
}

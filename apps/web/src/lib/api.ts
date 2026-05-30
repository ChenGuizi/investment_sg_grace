import type { DeepResearchReport, MarketSummary, NewsArticle, PortfolioSummary, PricePoint, Quote } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}/api${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {})
    },
    next: { revalidate: 30 }
  });
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }
  return response.json();
}

export const api = {
  marketSummary: () => request<MarketSummary>("/market/summary"),
  quote: (ticker: string) => request<Quote>(`/stocks/${ticker}/quote`),
  prices: (ticker: string) => request<PricePoint[]>(`/stocks/${ticker}/prices?days=180`),
  news: (ticker: string) => request<NewsArticle[]>(`/stocks/${ticker}/news`),
  research: (ticker: string) => request<DeepResearchReport>(`/research/${ticker}`),
  portfolio: () =>
    request<PortfolioSummary>("/portfolio/summary", {
      method: "POST",
      body: JSON.stringify({
        holdings: [
          { ticker: "NVDA", quantity: 8, average_cost: 215 },
          { ticker: "MSFT", quantity: 10, average_cost: 330 },
          { ticker: "D05.SI", quantity: 100, average_cost: 35.5 },
          { ticker: "O39.SI", quantity: 200, average_cost: 12.7 }
        ]
      })
    })
};

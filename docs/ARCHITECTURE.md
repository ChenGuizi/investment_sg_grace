# Architecture

## Runtime Components

- Next.js dashboard for investors.
- FastAPI backend for data access, agent orchestration, reporting, portfolio analysis, auth, audit, and scheduler jobs.
- PostgreSQL for users, portfolios, watchlists, audit events, and generated research reports.
- Vector database adapter slot for Pinecone or Weaviate.
- Provider adapters for market data, fundamentals, technicals, news, AI models, and email delivery.

## Agent Flow

1. Market Research Agent collects index, macro, earnings, and market context.
2. News Intelligence Agent deduplicates, ranks, and scores article impact.
3. Fundamental Analysis Agent scores growth, margins, cash flow, returns, debt, and valuation.
4. Technical Analysis Agent scores trend, RSI, MACD, support/resistance, SMA, and EMA.
5. Risk Agent assesses beta, volatility, earnings, market, regulatory, and concentration risk.
6. Recommendation Agent combines weighted findings into Buy/Hold/Sell with confidence.
7. Portfolio Advisor Agent reviews holdings, P/L, allocation, and rebalancing.
8. Critic Agent checks for missing evidence, missing risks, and contradictory conclusions.

## Data Provider Strategy

The repository ships with deterministic demo providers so the app can run immediately. Production deployment should replace them with provider-specific implementations:

- US market data: Polygon, Finnhub, IEX Cloud, Alpha Vantage, Yahoo Finance fallback.
- Singapore data: SGX announcements, Yahoo Finance `.SI`, broker feeds, or licensed SGX data.
- News: Reuters, Bloomberg, CNBC, FT, WSJ, company press releases, SGX announcements.
- AI: OpenAI, Anthropic Claude, or a routing layer.
- Email: Gmail API OAuth or SendGrid.

## Explainability Contract

Every recommendation must include:

- action
- confidence
- reasons
- risks
- evidence
- citations when available
- critic notes

The API schema makes this visible to the UI and downstream email reports.

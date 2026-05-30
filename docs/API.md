# API

Base path: `/api`

## Core

- `GET /health`
- `GET /monitoring/readiness`

## Market

- `GET /market/summary`

## Stocks

- `GET /stocks/{ticker}/quote`
- `GET /stocks/{ticker}/prices?days=180`
- `GET /stocks/{ticker}/news`
- `GET /stocks/{ticker}/fundamentals`
- `GET /stocks/{ticker}/technicals`

## Research

- `GET /research/{ticker}`
- `GET /research/{ticker}/knowledge-graph`

## Portfolio

- `POST /portfolio/summary`

```json
{
  "holdings": [
    { "ticker": "NVDA", "quantity": 8, "average_cost": 215 },
    { "ticker": "D05.SI", "quantity": 100, "average_cost": 35.5 }
  ]
}
```

## Reports

- `POST /reports/daily`
- `POST /reports/daily/email`

## Auth

- `POST /auth/register`

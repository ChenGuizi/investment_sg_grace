from datetime import datetime, timedelta
from math import sin

from app.schemas.market import FundamentalMetrics, PricePoint, StockQuote, TechnicalMetrics


class MarketDataProvider:
    async def quote(self, ticker: str) -> StockQuote:
        raise NotImplementedError

    async def prices(self, ticker: str, days: int = 260) -> list[PricePoint]:
        raise NotImplementedError

    async def fundamentals(self, ticker: str) -> FundamentalMetrics:
        raise NotImplementedError

    async def technicals(self, ticker: str) -> TechnicalMetrics:
        raise NotImplementedError


class DemoMarketDataProvider(MarketDataProvider):
    names = {
        "AAPL": ("Apple", "US", "USD", "Technology"),
        "NVDA": ("Nvidia", "US", "USD", "Semiconductors"),
        "MSFT": ("Microsoft", "US", "USD", "Technology"),
        "D05.SI": ("DBS Group", "SG", "SGD", "Financials"),
        "O39.SI": ("OCBC", "SG", "SGD", "Financials"),
        "U11.SI": ("UOB", "SG", "SGD", "Financials"),
        "9CI.SI": ("CapitaLand Investment", "SG", "SGD", "Real Estate"),
        "^GSPC": ("S&P 500", "US", "USD", "Index"),
        "^IXIC": ("Nasdaq Composite", "US", "USD", "Index"),
        "^STI": ("Straits Times Index", "SG", "SGD", "Index"),
    }

    def _base(self, ticker: str) -> float:
        return 45 + (sum(ord(c) for c in ticker) % 350)

    async def quote(self, ticker: str) -> StockQuote:
        ticker = ticker.upper()
        name, market, currency, sector = self.names.get(ticker, (ticker, "US", "USD", "Unknown"))
        base = self._base(ticker)
        change_percent = ((sum(ord(c) for c in ticker) % 15) - 5) / 100
        price = round(base * (1 + change_percent), 2)
        return StockQuote(
            ticker=ticker,
            name=name,
            market=market,
            currency=currency,
            price=price,
            change=round(base * change_percent, 2),
            change_percent=round(change_percent * 100, 2),
            sector=sector,
            updated_at=datetime.utcnow(),
        )

    async def prices(self, ticker: str, days: int = 260) -> list[PricePoint]:
        base = self._base(ticker)
        now = datetime.utcnow()
        rows: list[PricePoint] = []
        for i in range(days):
            dt = now - timedelta(days=days - i)
            drift = i * 0.08
            wave = sin(i / 9) * 4
            close = round(base + drift + wave, 2)
            rows.append(
                PricePoint(
                    date=dt,
                    open=round(close * 0.995, 2),
                    high=round(close * 1.018, 2),
                    low=round(close * 0.982, 2),
                    close=close,
                    volume=1_000_000 + i * 2311,
                )
            )
        return rows

    async def fundamentals(self, ticker: str) -> FundamentalMetrics:
        seed = sum(ord(c) for c in ticker)
        return FundamentalMetrics(
            ticker=ticker.upper(),
            revenue_growth=round(0.05 + (seed % 22) / 100, 3),
            eps_growth=round(0.03 + (seed % 28) / 100, 3),
            operating_margin=round(0.18 + (seed % 20) / 100, 3),
            free_cash_flow_yield=round(0.025 + (seed % 9) / 100, 3),
            roe=round(0.11 + (seed % 18) / 100, 3),
            roic=round(0.09 + (seed % 14) / 100, 3),
            debt_to_equity=round(0.25 + (seed % 85) / 100, 2),
            pe=round(12 + seed % 42, 2),
            forward_pe=round(10 + seed % 36, 2),
            peg=round(0.8 + (seed % 24) / 10, 2),
            price_to_book=round(1.2 + (seed % 60) / 10, 2),
            ev_to_ebitda=round(8 + seed % 25, 2),
        )

    async def technicals(self, ticker: str) -> TechnicalMetrics:
        prices = await self.prices(ticker)
        closes = [p.close for p in prices]
        sma20 = sum(closes[-20:]) / 20
        sma50 = sum(closes[-50:]) / 50
        sma200 = sum(closes[-200:]) / 200
        current = closes[-1]
        trend = "Uptrend" if current > sma50 > sma200 else "Sideways" if current > sma200 else "Downtrend"
        return TechnicalMetrics(
            ticker=ticker.upper(),
            trend=trend,
            support=round(min(closes[-30:]), 2),
            resistance=round(max(closes[-30:]) * 1.03, 2),
            rsi=round(45 + (sum(ord(c) for c in ticker) % 35), 2),
            macd=round((sma20 - sma50) / 10, 2),
            sma20=round(sma20, 2),
            sma50=round(sma50, 2),
            sma200=round(sma200, 2),
            ema20=round((current * 0.18) + (sma20 * 0.82), 2),
        )


def get_market_data_provider() -> MarketDataProvider:
    return DemoMarketDataProvider()

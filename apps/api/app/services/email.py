import base64
from email.message import EmailMessage

import httpx

from app.core.config import Settings
from app.schemas.common import Citation
from app.schemas.market import DailyReport, StockRecommendation


class EmailService:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def send_daily_report(self, recipient: str, report: DailyReport) -> dict:
        subject = f"Daily Stock Intelligence Report - {report.report_date}"
        body = self._render(report)
        if self.settings.sendgrid_api_key:
            return await self._send_with_sendgrid(recipient, subject, body)
        if self.settings.gmail_refresh_token:
            return await self._send_with_gmail(recipient, subject, body)
        return {
            "status": "dry_run",
            "to": recipient,
            "subject": subject,
            "body_preview": body[:500],
        }

    async def _send_with_sendgrid(self, recipient: str, subject: str, body: str) -> dict:
        payload = {
            "personalizations": [{"to": [{"email": recipient}]}],
            "from": {"email": self.settings.email_from},
            "subject": subject,
            "content": [{"type": "text/plain", "value": body}],
        }
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={"Authorization": f"Bearer {self.settings.sendgrid_api_key}"},
                json=payload,
            )
            response.raise_for_status()
        return {"status": "sent", "provider": "sendgrid", "to": recipient, "subject": subject}

    async def _send_with_gmail(self, recipient: str, subject: str, body: str) -> dict:
        if not self.settings.gmail_client_id or not self.settings.gmail_client_secret:
            return {"status": "dry_run", "reason": "gmail_oauth_not_configured", "to": recipient, "subject": subject}
        async with httpx.AsyncClient(timeout=20) as client:
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "client_id": self.settings.gmail_client_id,
                    "client_secret": self.settings.gmail_client_secret,
                    "refresh_token": self.settings.gmail_refresh_token,
                    "grant_type": "refresh_token",
                },
            )
            token_response.raise_for_status()
            access_token = token_response.json()["access_token"]
            message = EmailMessage()
            message["To"] = recipient
            message["From"] = self.settings.email_from
            message["Subject"] = subject
            message.set_content(body)
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_response = await client.post(
                "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
                headers={"Authorization": f"Bearer {access_token}"},
                json={"raw": raw},
            )
            send_response.raise_for_status()
        return {"status": "sent", "provider": "gmail", "to": recipient, "subject": subject}

    def _render(self, report: DailyReport) -> str:
        buys = self._render_recommendations(report.top_buy_ideas)
        holds = self._render_recommendations(report.hold_ideas)
        sells = self._render_recommendations(report.sell_alerts)
        watchlist = "\n".join(f"- {ticker}" for ticker in report.stocks_to_watch)
        market_news = "\n".join(f"- {event}" for event in report.market_summary.macro_events)
        news_references = self._render_news_references(report)
        suggestions = self._render_suggestions(report)
        return f"""
Market Summary
{report.market_summary.ai_summary}

Summarized News and Market Drivers
{market_news or "- No major market drivers detected today"}
{news_references}

Top Buy Ideas
{buys or "- No buy ideas today"}

Hold Ideas
{holds or "- No hold ideas today"}

Sell Alerts
{sells or "- No sell alerts today"}

Stocks to Watch
{watchlist or "- No watchlist alerts today"}

Suggestions
{suggestions}

Major Risks
{chr(10).join(f"- {risk}" for risk in report.major_risks_today)}

Open the dashboard: {self.settings.web_app_url}
""".strip()

    def _render_recommendations(self, recommendations: list[StockRecommendation]) -> str:
        rows = []
        for recommendation in recommendations:
            reason = recommendation.reasons[0] if recommendation.reasons else "Agent score changed today."
            risk = recommendation.risks[0] if recommendation.risks else "Monitor position sizing and news flow."
            target = f", target {recommendation.target_price}" if recommendation.target_price else ""
            rows.append(
                f"- {recommendation.ticker}: {recommendation.action} "
                f"({recommendation.confidence:.0f}% confidence{target})\n"
                f"  Why: {reason}\n"
                f"  Watch: {risk}"
            )
        return "\n".join(rows)

    def _render_news_references(self, report: DailyReport) -> str:
        citations: list[Citation] = []
        for recommendation in [*report.top_buy_ideas, *report.hold_ideas, *report.sell_alerts]:
            for evidence in recommendation.evidence:
                citations.extend(evidence.citations)
        unique = {citation.url: citation for citation in citations}
        if not unique:
            return ""
        rows = [f"- {citation.title} ({citation.publisher})" for citation in list(unique.values())[:8]]
        return "\nNews References\n" + "\n".join(rows)

    def _render_suggestions(self, report: DailyReport) -> str:
        suggestions = [
            "Review new BUY ideas against your existing sector exposure before adding positions.",
            "Use SELL alerts as a prompt to verify thesis deterioration, not as an automatic trade instruction.",
            "Keep position sizes smaller for high-valuation technology names when rate risk is rising.",
        ]
        if report.portfolio_summary:
            suggestions.extend(report.portfolio_summary.recommendations)
        return "\n".join(f"- {suggestion}" for suggestion in suggestions)

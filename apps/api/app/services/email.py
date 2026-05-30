from app.core.config import Settings
from app.schemas.market import DailyReport


class EmailService:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def send_daily_report(self, recipient: str, report: DailyReport) -> dict:
        subject = f"Daily Stock Intelligence Report - {report.report_date}"
        body = self._render(report)
        # Production adapters should call Gmail API or SendGrid here.
        return {
            "status": "queued" if self.settings.sendgrid_api_key or self.settings.gmail_refresh_token else "dry_run",
            "to": recipient,
            "subject": subject,
            "body_preview": body[:500],
        }

    def _render(self, report: DailyReport) -> str:
        buys = "\n".join(f"- {r.ticker}: {r.action} ({r.confidence:.0f}%) - {r.reasons[0]}" for r in report.top_buy_ideas)
        holds = "\n".join(f"- {r.ticker}: {r.action} ({r.confidence:.0f}%)" for r in report.hold_ideas)
        sells = "\n".join(f"- {r.ticker}: {r.action} ({r.confidence:.0f}%) - {r.risks[0] if r.risks else 'Risk elevated'}" for r in report.sell_alerts)
        return f"""
Market Summary
{report.market_summary.ai_summary}

Top Buy Ideas
{buys or "- No buy ideas today"}

Hold Ideas
{holds or "- No hold ideas today"}

Sell Alerts
{sells or "- No sell alerts today"}

Major Risks
{chr(10).join(f"- {risk}" for risk in report.major_risks_today)}

Open the dashboard: {self.settings.web_app_url}
""".strip()

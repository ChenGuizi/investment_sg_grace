from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from structlog import get_logger

from app.agents.orchestrator import ResearchOrchestrator
from app.core.config import Settings
from app.providers.market_data import get_market_data_provider
from app.providers.news import get_news_provider
from app.services.email import EmailService
from app.services.reporting import DailyReportService

logger = get_logger()


def create_scheduler(settings: Settings) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=ZoneInfo("Asia/Singapore"))

    async def daily_report_job() -> None:
        logger.info(
            "daily_report_job_started",
            hour=settings.daily_report_hour_sgt,
            recipient=settings.daily_report_recipient,
        )
        market_data = get_market_data_provider()
        news = get_news_provider()
        orchestrator = ResearchOrchestrator(market_data, news)
        report = await DailyReportService(market_data, orchestrator).generate()
        result = await EmailService(settings).send_daily_report(settings.daily_report_recipient, report)
        logger.info(
            "daily_report_job_finished",
            recipient=settings.daily_report_recipient,
            status=result["status"],
        )

    scheduler.add_job(
        daily_report_job,
        "cron",
        hour=settings.daily_report_hour_sgt,
        minute=0,
        id="daily-stock-intelligence-report",
        replace_existing=True,
    )
    return scheduler

from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from structlog import get_logger

from app.core.config import Settings

logger = get_logger()


def create_scheduler(settings: Settings) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=ZoneInfo("Asia/Singapore"))

    async def daily_report_job() -> None:
        logger.info("daily_report_job_started", hour=settings.daily_report_hour_sgt)
        # In production, fetch opted-in users, generate personalized reports, and deliver email.

    scheduler.add_job(
        daily_report_job,
        "cron",
        hour=settings.daily_report_hour_sgt,
        minute=0,
        id="daily-stock-intelligence-report",
        replace_existing=True,
    )
    return scheduler

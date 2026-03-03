import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from datetime import datetime

from config.config import settings
from notifer.notifier import Notifier
from client.api import APIClient

class NotificationScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler(
            jobstores={'default': MemoryJobStore()},
            timezone=pytz.timezone(settings["NOTIFICATION_TIMEZONE"]),
            job_defaults={
                'coalesce': True,
                'max_instances': 1,
                'misfire_grace_time': settings["SCHEDULER_MISFIRE_GRACE_TIME"]
            }
        )
        self.notifier = Notifier()

    def is_working_day(self) -> bool:
        if settings["INCLUDE_WEEKENDS"]:
            return True
        tz = pytz.timezone(settings.NOTIFICATION_TIMEZONE)
        now = datetime.now(tz)
        # Понедельник = 0, Воскресенье = 6
        # 0-4 это пн-пт
        return now.weekday() < 5

    async def send_daily_notifications(self):
        if not self.is_working_day():
            return
        try:
            client = APIClient()
            managers = await client.do_request()
            if not managers:
                return
            await self.notifier.send_bulk_notifications(managers)
        except Exception as e:
            pass

    def start(self):
        # Создаем триггер на каждый день в 8:00
        trigger = CronTrigger(
            hour=settings["NOTIFICATION_HOUR"],
            minute=settings["NOTIFICATION_MINUTE"],
            timezone=pytz.timezone(settings["NOTIFICATION_TIMEZONE"])
        )
        self.scheduler.add_job(
            self.send_daily_notifications,
            trigger=trigger,
            id='daily_notifications',
            name='Send daily notifications to managers'
        )

        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()

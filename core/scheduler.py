from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .tasks import update_history_stock


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        update_history_stock,
        trigger=CronTrigger(hour="12", minute="30"),
        id="update_history_stock",
        name="Update history stock daily at 16:00",
        replace_existing=True,
    )
    scheduler.start()

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from tjpowertracker import TJPowerTracker
from config import config
from emailhelper import send_remaining
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format="[{levelname}] {asctime} {name} {message}", style="{", level="INFO")


tracker = TJPowerTracker(
    username=config.username,
    password=config.password,
)


def get_and_send():
    remaining = tracker.get_remaining()
    print(remaining)
    for recipient in config.email_list:
        send_remaining(config.smtp['username'], recipient, remaining, config.smtp['password'])


scheduler = BlockingScheduler()
scheduler.add_job(get_and_send, CronTrigger(hour=12))
# scheduler.add_job(get_and_send, IntervalTrigger(seconds=15))
logging.info("Starting scheduler...")
scheduler.start()

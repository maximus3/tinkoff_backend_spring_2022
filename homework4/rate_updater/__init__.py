import logging

from apscheduler.schedulers.background import BackgroundScheduler

from database.views import update_rates

logging.basicConfig(
    level=logging.INFO,
    filename='app.log',
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_rates, 'interval', seconds=10)
    scheduler.start()
    return scheduler

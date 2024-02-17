import schedule
from src.cron_jobs import control_append_db
import time


def scheduled_task():
    schedule.every().monday.at("03:40").do(control_append_db.append_votes)
    schedule.every().monday.at("04:00").do(control_append_db.append_parties)
    schedule.every().monday.at("04:10").do(control_append_db.append_politicians)

    print("Cronjob executed!")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    scheduled_task()

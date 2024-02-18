import schedule
from src.cron_jobs import control_append_db
import time


def scheduled_task():
    schedule.every().day.at("09:05").do(control_append_db.append_votes_json)
    schedule.every().day.at("09:06").do(control_append_db.append_parties)
    schedule.every().day.at("09:07").do(control_append_db.append_politicians_json)

    print("Cronjob executed!")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    scheduled_task()

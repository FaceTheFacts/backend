import datetime
from dateutil.relativedelta import relativedelta


def get_last_day_of_the_month():
    last_day_of_the_month = None

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    if tomorrow.month != today.month:
        last_day_of_the_month = today
    else:
        last_day_of_the_month = datetime.date(
            today.year, today.month, 1
        ) - datetime.timedelta(days=1)

    return last_day_of_the_month

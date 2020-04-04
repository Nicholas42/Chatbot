from datetime import datetime

import pytz


def format_date(date: datetime, fmt="%d.%m.%Y %H:%M:%S"):
    return date.astimezone(pytz.timezone("Europe/Berlin")).strftime(fmt)

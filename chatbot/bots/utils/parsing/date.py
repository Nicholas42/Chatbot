from datetime import datetime

from dateparser import parse


def parse_date(s: str, *args, **kwargs) -> datetime:
    _SETTINGS = {"PREFER_DATES_FROM": "future", "DATE_ORDER": "DMY"}
    return parse(s, *args, languages=["de", "en"], settings=_SETTINGS, **kwargs)

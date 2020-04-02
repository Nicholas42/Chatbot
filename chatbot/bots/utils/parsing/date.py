from datetime import datetime

from dateparser import parse


def parse_date(s: str, *args, **kwargs) -> datetime:
    _SETTINGS = {"PREFER_DATES_FROM": "future", "DATE_ORDER": "DMY", "RETURN_AS_TIMEZONE_AWARE": True,
                 "TIMEZONE": "Europe/Berlin"}
    ret = parse(s, *args, languages=["de"], settings=_SETTINGS, **kwargs)
    if not ret:
        return parse(s, *args, settings=_SETTINGS, **kwargs)
    return ret

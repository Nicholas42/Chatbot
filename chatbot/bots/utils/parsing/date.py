from datetime import datetime

from dateparser import parse
from dateutil.parser import parserinfo


def parse_date(s: str, *args, **kwargs) -> datetime:
    _SETTINGS = {"PREFER_DATES_FROM": "future", "DATE_ORDER": "DMY"}
    return parse(s, *args, languages=["de", "en"], settings=_SETTINGS, **kwargs)


class ParserInfo(parserinfo):
    JUMP = [" ", ".", ",", ";", "-", "/", "'", "und", "am", "des"]

    WEEKDAYS = [("Mon", "Monday", "Mo", "Montag"),
                ("Tue", "Tuesday", "Di", "Dienstag"),
                ("Wed", "Wednesday", "Mi", "Mittwoch"),
                ("Thu", "Thursday", "Do", "Donnerstag"),
                ("Fri", "Friday", "Fr", "Freitag"),
                ("Sat", "Saturday", "Sa", "Samstag"),
                ("Sun", "Sunday", "So", "Sonntag")]
    MONTHS = [("Jan", "January", "Januar"),
              ("Feb", "February", "Februar"),
              ("Mar", "March", "März", "Mär"),
              ("Apr", "April"),
              ("May", "May", "Mai"),
              ("Jun", "June", "Juni"),
              ("Jul", "July", "Juli"),
              ("Aug", "August"),
              ("Sep", "Sept", "September"),
              ("Oct", "October", "Okt", "Oktober"),
              ("Nov", "November"),
              ("Dec", "December", "Dez", "Dezember")]
    HMS = [("h", "hour", "hours", "stunde", "stunden"),
           ("m", "minute", "minutes", "minuten", "min"),
           ("s", "second", "seconds", "sek", "sekunde", "sekunden")]
    AMPM = [("am", "a"),
            ("pm", "p")]
    UTCZONE = ["UTC", "GMT", "Z", "z"]
    PERTAIN = []
    TZOFFSET = {}

    def __init__(self):
        super().__init__(dayfirst=True, yearfirst=False)

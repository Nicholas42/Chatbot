from datetime import datetime
from enum import Enum, auto

import pytz

from chatbot.config import config


class MessageType(Enum):
    post = auto()
    ping = auto()
    pong = auto()
    ack = auto()


def parse_date(text: str, tzinfo=pytz.timezone("Europe/Berlin")) -> datetime:
    return tzinfo.localize(datetime.strptime(text, config["message"]["dateformat"]))


def format_date(date: datetime, tzinfo=pytz.timezone("Europe/Berlin")) -> str:
    return date.astimezone(tzinfo).strftime(config["message"]["dateformat"])


class Color:
    def __init__(self, hex_str: str):
        self.r = int(hex_str[0:2], 16)
        self.g = int(hex_str[2:4], 16)
        self.b = int(hex_str[4:6], 16)

    def to_hex(self):
        return "".join(hex(i)[2:] for i in [self.r, self.g, self.b])

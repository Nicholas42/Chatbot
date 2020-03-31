from datetime import datetime
from enum import Enum, auto

from chatbot import glob


class MessageType(Enum):
    post = auto()
    ping = auto()
    pong = auto()
    ack = auto()


def parse_date(text: str) -> datetime:
    return datetime.strptime(text, glob.config["message"]["dateformat"])


def format_date(date: datetime) -> str:
    return date.strftime(glob.config["message"]["dateformat"])


class Color:
    def __init__(self, hex_str: str):
        self.r = int(hex_str[0:2], 16)
        self.g = int(hex_str[2:4], 16)
        self.b = int(hex_str[4:6], 16)

    def to_hex(self):
        return "".join(hex(i)[2:] for i in [self.r, self.g, self.b])

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

from chatbot.interface.message_helpers import MessageType, Color, parse_date


@dataclass
class IncomingMessage:
    id: int
    name: str
    message: str
    channel: str
    date: datetime
    user_id: Optional[int]
    username: Optional[str]
    delay: int
    bottag: bool
    type: MessageType
    color: Color

    @classmethod
    def from_json(cls, json_text: str):
        return cls.from_dict(json.loads(json_text))

    @classmethod
    def from_dict(cls, d: dict):
        d["date"] = parse_date(d["date"])
        d["bottag"] = bool(d["bottag"])
        d["type"] = MessageType[d["type"]]
        d["color"] = Color(d["color"])

        return IncomingMessage(**d)


@dataclass
class OutgoingMessage:
    channel: str
    name: str
    message: str
    delay: int = 0
    publicid: int = 1

    def to_dict(self) -> dict:
        d = asdict(self)
        # If it is a bool otherwise
        d["publicid"] = int(d["publicid"])

        return d

    def to_json(self) -> str:
        d = self.to_dict()
        return json.dumps(d)

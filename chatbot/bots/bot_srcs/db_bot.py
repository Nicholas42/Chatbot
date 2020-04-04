from chatbot.bots.base import BaseBot
from chatbot.database.db import database
from chatbot.database.messages import IncomingMessageModel
from chatbot.interface.messages import IncomingMessage


class DBBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.react_on_bots = True

    async def _react(self, incoming: IncomingMessage):
        with database.context as session:
            model = IncomingMessageModel.construct(incoming)
            session.add(model)


def create_bot(*args, **kwargs):
    return DBBot()

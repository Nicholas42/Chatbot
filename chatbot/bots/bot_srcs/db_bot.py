from chatbot import glob
from chatbot.bots.base import BaseBot
from chatbot.database.messages import IncomingMessageModel
from chatbot.interface.messages import IncomingMessage


class DBBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.react_on_bots = True

    @property
    def session(self):
        return glob.db.session

    async def _react(self, incoming: IncomingMessage):
        model = IncomingMessageModel.construct(incoming)
        self.session.add(model)
        self.session.commit()
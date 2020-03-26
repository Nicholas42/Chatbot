from asyncio import as_completed
from typing import Dict

from chatbot.bots.abc import BotABC
from chatbot.bots.loader import Loader


class BotMaster:
    bots: Dict[str, BotABC]

    def __init__(self):
        self.loader = Loader()
        self.bots = dict()

    async def react(self, msg_queue):
        msg = await msg_queue.get()
        for i in as_completed([i.react(msg) for i in self.bots.values()]):
            ret = await i

    def load_bot(self, bot_name):
        self.bots[bot_name] = self.loader.create_bot(bot_name)

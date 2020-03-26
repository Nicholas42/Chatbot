from asyncio import as_completed
from typing import Dict

from chatbot.bots.abc import BotABC
from chatbot.bots.loader import Loader
from chatbot.interface.bridge import Bridge


class BotMaster:
    loader: Loader
    bots: Dict[str, BotABC]
    bridge: Bridge

    def __init__(self, bridge: Bridge):
        self.loader = Loader()
        self.bots = dict()
        self.bridge = bridge

    async def react(self):
        msg = await self.bridge.get_incoming()
        for i in as_completed([i.react(msg) for i in self.bots.values()]):
            ret = await i
            if ret:
                self.bridge.put_outgoing_nowait(ret)

    async def stop_bot(self, bot_name):
        bot = self.bots.pop(bot_name)
        await bot.shutdown()

    async def reload_bot(self, bot_name):
        await self.stop_bot(bot_name)
        self.loader.reload_bot(bot_name)
        self.load_bot(bot_name)

    def load_bot(self, bot_name):
        self.bots[bot_name] = self.loader.create_bot(bot_name)

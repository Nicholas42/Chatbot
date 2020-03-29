from asyncio import as_completed, create_task, CancelledError, wait
from typing import Dict

from chatbot import config
from chatbot.bots import module_logger
from chatbot.bots.base import BaseBot
from chatbot.bots.loader import Loader
from chatbot.interface.bridge import Bridge

logger = module_logger.getChild("botmaster")


class BotMaster:
    loader: Loader
    bots: Dict[str, BaseBot]
    bridge: Bridge

    def __init__(self, bridge: Bridge, _config=None):
        if _config is None:
            _config = config
        self.loader = Loader()
        self.bots = dict()
        self.bridge = bridge
        self.listening_task = create_task(self.run())

        for i in _config["botmaster"]["default_bots"]:
            self.load_bot(i)

    async def run(self):
        while True:
            try:
                await self.react()
            except Exception as e:
                logger.exception(e)

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
        self.bots[bot_name] = self.loader.create_bot(bot_name, self)

    async def shutdown(self):
        try:
            self.listening_task.cancel()
            await self.listening_task
        except CancelledError:
            pass

        await wait([i.shutdown() for i in self.bots.values()])

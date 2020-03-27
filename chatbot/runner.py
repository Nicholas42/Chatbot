from asyncio import wait

from chatbot import config
from chatbot.bots.botmaster import BotMaster
from chatbot.connection.chat import Chat
from chatbot.interface.bridge import Bridge


class Runner:
    def __init__(self, _config=None):
        if _config is None:
            _config = config
        self.bridge = Bridge()
        self.chat = Chat(self.bridge, _config)
        self.botmaster = BotMaster(self.bridge, _config)

    async def wait_running(self):
        await wait([self.botmaster.listening_task, self.chat.send_task])

    async def shutdown(self):
        await self.chat.shutdown()
        await self.botmaster.shutdown()
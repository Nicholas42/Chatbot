from aioconsole.console import interact
from aioconsole.server import start_console_server

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
        self.server = None

    async def wait_running(self):
        d = locals().copy()
        d["botmaster"] = self.botmaster
        d["bridge"] = self.bridge
        d["chat"] = self.chat
        d["exit"] = lambda: self.server.close()

        self.server = await start_console_server(host="0.0.0.0", port=5000, locals=d)
        await self.server.wait_closed()

    async def shutdown(self):
        await self.chat.shutdown()
        await self.botmaster.shutdown()

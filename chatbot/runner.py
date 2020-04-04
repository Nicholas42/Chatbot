from aioconsole.server import start_console_server

from .bots.botmaster import BotMaster
from .config import config
from .connection.chat import Chat
from .database.db import database
from .interface.bridge import Bridge


class Runner:
    def __init__(self, _config=None):
        if _config is not None:
            config.load(_config.path, config.env_file)

        self.server = None
        self.bridge = Bridge()
        self.chat = Chat(self.bridge)
        self.botmaster = BotMaster(self.bridge)

    async def wait_running(self):
        d = locals().copy()
        d["botmaster"] = self.botmaster
        d["bridge"] = self.bridge
        d["chat"] = self.chat
        d["db"] = database
        d["exit"] = lambda: self.server.close()

        self.server = await start_console_server(host="0.0.0.0", port=5001, locals=d)
        await self.server.wait_closed()

    async def shutdown(self):
        self.server.close()
        await self.chat.shutdown()
        await self.botmaster.shutdown()

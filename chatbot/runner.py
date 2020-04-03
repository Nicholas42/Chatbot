from aioconsole.server import start_console_server

from chatbot import glob
from chatbot.config import Config


class Runner:
    def __init__(self, _config=None):
        if _config is None:
            _config = Config()
        glob.config = _config
        self.server = None

    async def wait_running(self):
        d = locals().copy()
        glob.start_all()
        d["botmaster"] = glob.botmaster
        d["bridge"] = glob.bridge
        d["chat"] = glob.chat
        d["db"] = glob.db
        d["exit"] = lambda: self.server.close()

        self.server = await start_console_server(host="0.0.0.0", port=5001, locals=d)
        await self.server.wait_closed()

    @staticmethod
    async def shutdown():
        await glob.chat.shutdown()
        await glob.botmaster.shutdown()

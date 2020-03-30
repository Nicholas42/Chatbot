from aioconsole.server import start_console_server

from chatbot import glob, Config


class Runner:
    def __init__(self, _config=None):
        if _config is None:
            _config = Config()
        glob.config = _config
        self.server = None

    async def wait_running(self):
        d = locals().copy()
        d["botmaster"] = glob.botmaster
        d["bridge"] = glob.bridge
        d["chat"] = glob.chat
        d["exit"] = lambda: self.server.close()

        self.server = await start_console_server(host="0.0.0.0", port=5000, locals=d)
        await self.server.wait_closed()

    async def shutdown(self):
        await glob.chat.shutdown()
        await glob.botmaster.shutdown()

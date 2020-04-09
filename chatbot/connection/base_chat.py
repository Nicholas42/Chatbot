from abc import ABCMeta, abstractmethod
from asyncio import CancelledError, Task
from asyncio.tasks import create_task, wait
from typing import Dict

from chatbot.config import config
from chatbot.connection.chat import logger
from chatbot.interface.messages import IncomingMessage


class BaseChat(metaclass=ABCMeta):
    listener_tasks: Dict[str, Task]

    def __init__(self, bridge, _config=None):
        if _config is None:
            _config = config
        self.channels = dict()
        self.listener_tasks = dict()
        self.bridge = bridge
        self.send_task = create_task(self.send_worker())
        self.config = _config

        for i in _config["channel"]:
            self.listen(i)

    def handle_msg(self, msg: IncomingMessage):
        self.bridge.put_incoming_nowait(msg)

    async def send_worker(self):
        try:
            while True:
                msg = await self.bridge.get_outgoing()
                await self._send_msg(msg)
        except CancelledError:
            raise

    def listen(self, channel):
        logger.info(f"Registering channel {channel}.")
        self.channels[channel] = self._create_channel(channel)

        self.listener_tasks[channel] = create_task(self._listen_to(channel))
        logger.info(f"Registered channel {channel}.")

    async def unlisten(self, channel):
        logger.info(f"Unregistering channel {channel}.")
        try:
            self.listener_tasks[channel].cancel()
            await self.listener_tasks.pop(channel)
        except CancelledError:
            pass
        self.channels.pop(channel)

        logger.info(f"Unregistered channel {channel}.")

    async def shutdown(self):
        logger.info("Shutting down...")
        try:
            self.send_task.cancel()
            await self.send_task
        except CancelledError:
            pass
        await wait(map(self.unlisten, self.channels))
        logger.info("Shut down.")

    @abstractmethod
    def _send_msg(self, msg):
        pass

    @abstractmethod
    def _listen_to(self, channel):
        pass

    @abstractmethod
    def _create_channel(self, channel):
        pass

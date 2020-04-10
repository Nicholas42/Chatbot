import sys
from asyncio.events import get_running_loop
from asyncio.queues import Queue
from datetime import datetime, timezone

from .base_chat import BaseChat
from ..interface.message_helpers import MessageType, Color
from ..interface.messages import IncomingMessage

_BASE_MSG = {"id": 0, "name": "Nicholas", "username": "NicholasSchwab", "user_id": 412, "delay": 0, "bottag": 0,
             "type": MessageType.post, "color": Color("646464")}


class LocalChat(BaseChat):

    def __init__(self, bridge):
        super().__init__(bridge)
        self.queue = Queue()

    def _create_channel(self, channel):
        return channel

    async def _send_msg(self, msg):
        print(msg.to_dict())
        print(msg.message)

    async def _listen_to(self, channel):
        loop = get_running_loop()
        loop.add_reader(sys.stdin, lambda: self.queue.put_nowait(sys.stdin.readline()))

        while True:
            msg = await self.queue.get()
            self.handle_msg(
                IncomingMessage(message=msg, channel=channel, date=datetime.now(tz=timezone.utc), **_BASE_MSG))

from asyncio import create_task, Queue, CancelledError
from typing import Dict

from websockets import ConnectionClosedError

from .channel import Channel


class Chat:
    channels: Dict[str, Channel]

    def __init__(self):
        self.channels = dict()
        self.listener_tasks = dict()
        self.msg_queue = Queue()

    async def handle_msg(self, msg):
        await self.msg_queue.put(msg)

    def send_msg(self, message, channel=None):
        if channel is None:
            channel = message.get("channel")

        if channel not in self.channels:
            raise KeyError(f"Not listening to channel {channel}.")

        return create_task(self.channels[channel].send_msg(message))

    async def listen(self, channel):
        self.channels[channel] = Channel(channel)

        async def listen_to():
            try:
                while True:
                    conn = await self.channels[channel].start_listening()
                    try:
                        async for msg in conn:
                            await self.handle_msg(msg)
                    except ConnectionClosedError:
                        pass
                    await self.channels[channel].stop_listening()
            except CancelledError:
                await self.channels[channel].stop_listening()

        self.listener_tasks[channel] = create_task(listen_to())

    async def unlisten(self, channel):
        self.listener_tasks[channel].cancel()
        try:
            await self.listener_tasks[channel].cancel()
        except CancelledError:
            pass
        self.channels.pop(channel)

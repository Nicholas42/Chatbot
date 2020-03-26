from asyncio import create_task, Queue, CancelledError
from typing import Dict
import logging

from websockets import ConnectionClosedError

from .channel import Channel
from . import module_logger

logger: logging.Logger = module_logger.getChild("chat")


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
        logging.info(f"Registering channel {channel}.")
        self.channels[channel] = Channel(channel)

        async def listen_to():
            try:
                while True:
                    conn = await self.channels[channel].start_listening()
                    try:
                        async for msg in conn:
                            await self.handle_msg(msg)
                    except ConnectionClosedError as e:
                        logging.info(
                            f"Connection to channel {channel} closed with error.\n Code: {e.code}, Reason: {e.reason}")
                    await self.channels[channel].stop_listening()
                    logging.debug(f"Connection to channel {channel} closed, reconnecting...")
            except CancelledError:
                if channel in self.channels and self.channels[channel]:
                    await self.channels[channel].stop_listening()
                raise

        self.listener_tasks[channel] = create_task(listen_to())
        logger.info(f"Registered channel {channel}.")

    async def unlisten(self, channel):
        logger.info(f"Unregistering channel {channel}.")
        try:
            self.listener_tasks[channel].cancel()
            await self.listener_tasks[channel]
        except CancelledError:
            pass
        self.channels.pop(channel)
        self.listener_tasks.pop(channel)

        logger.info(f"Unregistered channel {channel}.")

import json
import logging
from asyncio import create_task, CancelledError, Task, wait
from typing import Dict

from websockets import ConnectionClosedError

from chatbot.interface.bridge import Bridge
from chatbot.interface.message_helpers import MessageType
from chatbot.interface.messages import IncomingMessage, OutgoingMessage
from . import module_logger
from .channel import Channel

logger: logging.Logger = module_logger.getChild("chat")


class Chat:
    channels: Dict[str, Channel]
    listener_tasks: Dict[str, Task]
    bridge: Bridge

    def __init__(self, bridge: Bridge):
        self.channels = dict()
        self.listener_tasks = dict()
        self.bridge = bridge
        self.send_task = create_task(self.send_worker())

    def handle_msg(self, msg: IncomingMessage):
        self.bridge.put_incoming_nowait(msg)

    async def send_worker(self):
        try:
            while True:
                msg = await self.bridge.get_outgoing()
                self._send_msg(msg)
        except CancelledError:
            raise

    def _send_msg(self, message: OutgoingMessage):
        channel = message.channel
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
                            self.handle_msg(IncomingMessage.from_json(msg))
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
            await self.listener_tasks.pop(channel)
        except CancelledError:
            pass
        self.channels.pop(channel)

        logger.info(f"Unregistered channel {channel}.")

    async def shutdown(self):
        logger.info("Shutting down...")
        self.send_task.cancel()
        await self.send_task
        await wait(map(self.unlisten, self.channels))
        logger.info("Shut down.")

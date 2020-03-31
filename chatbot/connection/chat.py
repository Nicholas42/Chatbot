import logging
from asyncio import create_task, CancelledError, Task, wait, sleep
from typing import Dict

from websockets import ConnectionClosedError

from chatbot import glob
from chatbot.interface.bridge import Bridge
from chatbot.interface.messages import IncomingMessage, OutgoingMessage
from . import module_logger
from .channel import Channel

logger: logging.Logger = module_logger.getChild("chat")


class Chat:
    channels: Dict[str, Channel]
    listener_tasks: Dict[str, Task]
    bridge: Bridge

    def __init__(self, bridge: Bridge, _config=None):
        if _config is None:
            _config = glob.config
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

    async def _send_msg(self, message: OutgoingMessage):
        channel = message.channel
        if channel not in self.channels:
            raise KeyError(f"Not listening to channel {channel}.")

        return await self.channels[channel].send_msg(message)

    def listen(self, channel):
        logger.info(f"Registering channel {channel}.")
        self.channels[channel] = Channel(channel, self.config)

        async def listen_to():
            try:
                while True:
                    conn = await self.channels[channel].start_listening()
                    try:
                        async for msg in conn:
                            self.handle_msg(IncomingMessage.from_json(msg))
                    except ConnectionClosedError as e:
                        logger.info(
                            f"Connection to channel {channel} closed with error.\n Code: {e.code}, Reason: {e.reason}")
                    except ConnectionResetError:
                        logger.info(f"Connection to channel {channel} reset by peer.")
                    except Exception as e:
                        logger.exception(e)
                        raise e
                    await self.channels[channel].stop_listening()
                    logger.debug(f"Connection to channel {channel} closed, reconnecting...")
                    await sleep(2)  # Give some time before reconnecting
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
        try:
            self.send_task.cancel()
            await self.send_task
        except CancelledError:
            pass
        await wait(map(self.unlisten, self.channels))
        logger.info("Shut down.")

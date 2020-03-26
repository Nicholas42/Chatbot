import json
import logging
from typing import Optional

from websockets import WebSocketClientProtocol

from .conn import PreparedConnection
from . import module_logger

logger: logging.Logger = module_logger.getChild("channel")


class Channel:
    listening_conn: Optional[WebSocketClientProtocol]

    def __init__(self, channel="test"):
        self.channel = channel
        self.connection = PreparedConnection(channel=channel, position=0)
        self.listening_conn = None

    async def start_listening(self):
        logger.debug(f"Start listening to channel {self.channel}.")
        self.listening_conn = await self.connection.connect()
        logger.debug(f"Connection to channel {self.channel} established.")
        return self.listening_conn

    async def read_msg(self):
        return await self.listening_conn.recv()

    async def stop_listening(self):
        logger.debug(f"Stop listening to channel {self.channel}.")
        await self.listening_conn.close()
        await self.listening_conn.wait_closed()
        self.listening_conn = None
        logger.debug(f"Connection to channel {self.channel} stopped.")

    async def send_msg(self, message):
        message["channel"] = self.channel
        message["publicid"] = 1 if message.get("publicid", 1) else 0
        message["delay"] = message.get("delay", 0)

        logger.debug(f"Sending message {message}.")

        async with self.connection.connect() as conn:
            await conn.send(json.dumps(message))

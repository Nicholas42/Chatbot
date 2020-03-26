import json
from typing import Optional

from websockets import WebSocketClientProtocol

from .conn import PreparedConnection


class Channel:
    listening_conn: Optional[WebSocketClientProtocol]

    def __init__(self, channel="test"):
        self.channel = channel
        self.connection = PreparedConnection(channel=channel, position=0)
        self.listening_conn = None

    async def start_listening(self):
        self.listening_conn = await self.connection.connect()
        return self.listening_conn

    async def read_msg(self):
        return await self.listening_conn.recv()

    async def stop_listening(self):
        await self.listening_conn.close()
        await self.listening_conn.wait_closed()
        self.listening_conn = None

    async def send_msg(self, message):
        message["channel"] = self.channel
        message["publicid"] = 1 if message.get("publicid", 1) else 0
        message["delay"] = message.get("delay", 0)

        async with self.connection.connect() as conn:
            await conn.send(json.dumps(message))

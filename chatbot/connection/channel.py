from websockets import WebSocketClientProtocol
import json

from .conn import Connection


class Channel:
    def __init__(self, channel="test"):
        self.channel = channel
        self.connection = await Connection(channel=channel, position=-1)

    async def send_msg(self, message, name, delay, publicid=True):
        d = {"message": message, "name": name, "publicid": publicid, "delay": delay, "channel": self.channel}
        conn: WebSocketClientProtocol
        return self.connection.send(json.dumps(d))

    async def read_msg(self):
        return self.connection.recv()

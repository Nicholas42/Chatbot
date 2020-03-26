from asyncio import Queue

from .messages import IncomingMessage, OutgoingMessage


class Bridge:
    incoming_queue: Queue[IncomingMessage]
    outgoing_queue: Queue[OutgoingMessage]

    def __init__(self):
        self.incoming_queue = Queue()
        self.outgoing_queue = Queue()

    async def get_incoming(self) -> IncomingMessage:
        return await self.incoming_queue.get()

    async def put_incoming(self, msg: IncomingMessage):
        await self.incoming_queue.put(msg)

    def put_incoming_nowait(self, msg: IncomingMessage):
        self.incoming_queue.put_nowait(msg)

    async def get_outgoing(self) -> OutgoingMessage:
        return await self.outgoing_queue.get()

    async def put_outgoing(self, msg: OutgoingMessage):
        await self.outgoing_queue.put(msg)

    def put_outgoing_nowait(self, msg: OutgoingMessage):
        self.outgoing_queue.put_nowait(msg)

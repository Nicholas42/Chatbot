from asyncio import CancelledError, sleep
from typing import Dict

from websockets import ConnectionClosedError

from chatbot.interface.messages import IncomingMessage, OutgoingMessage
from .base_chat import BaseChat, logger
from .channel import Channel


class Chat(BaseChat):
    channels: Dict[str, Channel]

    async def _send_msg(self, message: OutgoingMessage):
        channel = message.channel
        if channel not in self.channels:
            raise KeyError(f"Not listening to channel {channel}.")

        return await self.channels[channel].send_msg(message)

    async def _listen_to(self, channel):
        try:
            while True:
                try:
                    conn = await self.channels[channel].start_listening()
                except ConnectionError as e:
                    logger.exception("Connection reset when reconnecting, retrying", exc_info=e)
                    await sleep(10)
                    continue
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

    def _create_channel(self, channel):
        return Channel(channel, self.config)

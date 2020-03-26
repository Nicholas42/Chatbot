from abc import ABC, abstractmethod


class BotABC(ABC):
    @abstractmethod
    async def react(self, msg):
        pass

    @abstractmethod
    async def shutdown(self):
        pass

from chatbot.bots.base import BaseBot


class Echo(BaseBot):

    async def _react(self, message):
        print(message)


def create_bot(*_, **__):
    return Echo()

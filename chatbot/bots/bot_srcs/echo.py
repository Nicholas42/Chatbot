from chatbot.bots.abc import BotABC


class Echo:
    def __init__(self):
        pass

    async def react(self, message):
        print(message)


BotABC.register(Echo)


def create_bot():
    return Echo()

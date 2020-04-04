from ..base import BaseBot


class Echo(BaseBot):

    async def _react(self, message):
        print(message)


def create_bot(*args, **kwargs):
    return Echo()

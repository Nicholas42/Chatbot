from chatbot.bots.base import CommandBot
from chatbot.database.db import database
from chatbot.helpers.update.qedler import run


class UpdateBot(CommandBot):
    def __init__(self):
        super().__init__()
        self.name = "update"

    async def _react(self, msg):
        if msg.username == database.config["qeddb"]["username"]:
            return await super()._react(msg)
        return None


@UpdateBot.command()
def qedler(**kwargs):
    """ Updatet die interne QEDler Datenbank, wichtig für Nicknames """

    result = run()
    return f"{result['new_count'] - result['old_count']} neue QEDler eingetragen. " \
           f"Es sind jetzt insgesamt {result['new_count']}!"


def create_bot(*args, **kwargs):
    return UpdateBot()

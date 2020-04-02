from ..base import CommandBot
from ...helpers.update.qedler import run


class UpdateBot(CommandBot):
    def __init__(self):
        super().__init__()
        self.name = "update"


@UpdateBot.command("qedler")
def qedler(**kwargs):
    """ Updatet die interne QEDler Datenbank, wichtig für Nicknames """

    result = run()
    return f"{result['new_count'] - result['old_count']} neue QEDler eingetragen. " \
           f"Es sind jetzt insgesamt {result['new_count']}!"

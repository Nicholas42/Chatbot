import hashlib
import random

import pyparsing

from chatbot import glob
from chatbot.bots.base import BaseBot
from chatbot.bots.utils.parsing.command_parser import Parser, call_parse_result
from chatbot.bots.utils.parsing.common import uword
from chatbot.interface.messages import IncomingMessage
from chatbot.utils.async_sched import AsyncScheduler


def _lalala():
    length = random.randint(8, 14)
    return "la" + "a".join(random.choices(["l", "ll"], weights=[5, 1], k=length)) + "a"


class Luise(BaseBot):
    _time_out = 900  # seconds until luise renames herself back

    def __init__(self, config=None):
        super().__init__()
        if config is None:
            config = glob.config
        self.config = config["botmaster"]["default_bots"]["luise"]

        self.parser: pyparsing.ParserElement = pyparsing.Empty()
        self.botmaster = None
        self.rename_msg = None
        self.timer = AsyncScheduler(self._time_out, self._rename)

    def _rename(self):
        self.name = self.__class__.__name__
        self.botmaster.bridge.put_outgoing_nowait(self.create_msg("I am back! :-)", self.rename_msg))

    def reset_rename(self, message):
        if self.__class__.__name__ != self.name:
            self.rename_msg = message
            self.timer.reset(self._time_out)

    def reload_parsers(self):
        self.parser: pyparsing.ParserElement = pyparsing.Or(map(Parser.as_pp_parser, self.commands.values()))

    def get_keyword(self):
        return pyparsing.CaselessKeyword(f"!{self.name}")

    async def _react(self, msg: IncomingMessage):
        try:
            result = (self.get_keyword() + self.parser).parseString(msg.message)
        except pyparsing.ParseBaseException as e:
            return None

        self.reset_rename(msg)

        return call_parse_result(result, msg)


luise = Luise()


@luise.command()
def help(bot: Luise, **kwargs):
    """ Ich sag dir, wie du mit mir umgehen sollst! """

    help_msg = f"Hallo, ich bin {bot.name} und ich kann voooooooll tolle Sachen, zum Beispiel\n\n"
    return help_msg + "\n".join(f"{v.command_word}:\n\t {k.__doc__}" for k, v in bot.commands.items())


@luise.command({"name": "new_name", "value_parser": uword})
def be(bot, args, msg, **kwargs):
    """ Ich verwandel mich in jemand anderen! """
    bot.name = args["new_name"]
    bot.reset_rename(msg)

    return _lalala()


@luise.command()
def ping(**kwargs):
    """ Pong! """

    return "pong"


@luise.command()
def slap(args, **kwargs):
    """ Ich schlage jemanden! -.- """

    return f"*schlägt {args['_rest']}*"


@luise.command()
def hug(args, **kwargs):
    """ Ich knuddel jemanden! :-) """

    return f"*knuddelt {args['_rest']}*"


@luise.command()
def say(args, **kwargs):
    """ Ich sage etwas! """

    return args["_rest"]


@luise.command()
def decide(bot, args, **kwargs):
    """ Ich helfe dir, dich zu entscheiden! """
    salt = bot.config["secret"].encode()

    res = hashlib.sha256(args["_rest"].encode() + salt).digest()
    return '+' if int(res[0]) % 2 == 0 else '-'


@luise.command()
def featurerequest(args, **kwargs):
    """ Ich wünsch mir was! Und wenn ich gaaaaanz fest dran glaube wird es auch Wirklichkeit!"""

    return f"Ich will {args['_rest']}!"


def create_bot(botmaster):
    luise.botmaster = botmaster
    luise.reload_parsers()
    return luise

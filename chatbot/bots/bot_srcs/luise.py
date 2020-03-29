import hashlib

import pyparsing

from chatbot import config
from chatbot.bots.base import BaseBot
from chatbot.bots.utils.parsing.command_parser import Parser, call_parse_result
from chatbot.interface.messages import IncomingMessage


class Luise(BaseBot):
    def __init__(self):
        super().__init__()
        self.config = config["botmaster"]["default_bots"]["luise"]

        self.parser: pyparsing.ParserElement = pyparsing.Empty()

    def reload_parsers(self):
        self.parser: pyparsing.ParserElement = pyparsing.Or(map(Parser.as_pp_parser, self.commands.values()))

    def get_keyword(self):
        return pyparsing.CaselessKeyword(f"!{self.name}")

    async def react(self, msg: IncomingMessage):
        try:
            result = (self.get_keyword() + self.parser).parseString(msg.message)
        except pyparsing.ParseBaseException as e:
            return None

        return call_parse_result(result, msg)


luise = Luise()


@luise.command()
def help(bot: Luise, **kwargs):
    """ Ich sag dir, wie du mit mir umgehen sollst! """

    help_msg = f"Hallo, ich bin {bot.name} und ich kann voooooooll tolle Sachen, zum Beispiel\n\n"
    return help_msg + "\n".join(f"{v.command_word}:\n\t {k.__doc__}" for k, v in bot.commands.items())


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


def create_bot():
    luise.reload_parsers()
    return luise

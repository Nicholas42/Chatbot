import pyparsing

from chatbot.bots.abc import BotABC
from chatbot.bots.utils.parsing.command_parser import Parser, subparser, call_parse_result
from chatbot.bots.utils.parsing.common import rest_of_string
from chatbot.interface.messages import OutgoingMessage, IncomingMessage


class Luise:
    def __init__(self):
        self.name = "Luise"
        self.subs = []

        self.add_subparsers()
        self.parser: pyparsing.ParserElement = pyparsing.Or(self.subs)

    def create_msg(self, message, replying_to: IncomingMessage):
        return OutgoingMessage(channel=replying_to.channel, name=self.name, message=message,
                               delay=replying_to.delay + 1)

    def add_subparsers(self):
        for v in dir(self):
            func = getattr(self, v)
            if hasattr(func, "_subparser"):
                func()

    def get_keyword(self):
        return pyparsing.CaselessKeyword(f"!{self.name}")

    async def react(self, msg: IncomingMessage):
        try:
            result = (self.get_keyword() + self.parser).parseString(msg.message)
        except pyparsing.ParseBaseException:
            return None

        return call_parse_result(result, msg)

    @subparser
    def ping(self):
        def f(args, msg):
            return self.create_msg("pong", msg)

        sub = Parser("ping", func=f)
        self.subs.append(sub.as_pp_parser())

    @subparser
    def say(self):
        def f(args, msg):
            return self.create_msg(args["rest"], msg)

        sub = Parser("say", func=f)
        sub.add_positional_argument("rest", value_parser=rest_of_string)

        self.subs.append(sub.as_pp_parser())


BotABC.register(Luise)


def create_bot():
    return Luise()

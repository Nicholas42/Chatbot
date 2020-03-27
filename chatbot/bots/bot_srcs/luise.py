import pyparsing

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
        return OutgoingMessage(channel=replying_to.channel, name=self.name, message=message, delay=replying_to.delay)

    def add_subparsers(self):
        for k, v in self.__dict__.items():
            if hasattr(v, "_subparser"):
                v(self)

    async def react(self, msg: IncomingMessage):
        try:
            result = self.parser.parseString(msg.message)
        except pyparsing.ParseBaseException:
            return None

        return call_parse_result(result)

    @subparser
    def say(self):
        def f(args, msg):
            return self.create_msg("pong", msg)

        sub = Parser("say", func=f)
        self.subs.append(sub.as_pp_parser())

    @subparser
    def say(self):
        def f(args, msg):
            return self.create_msg(args["rest"], msg)

        sub = Parser("say", func=f)
        sub.add_positional_argument("rest", value_parser=rest_of_string)

        self.subs.append(sub.as_pp_parser())

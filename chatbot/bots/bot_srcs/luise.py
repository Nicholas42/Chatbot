import pyparsing

from chatbot.bots.abc import BotABC
from chatbot.bots.utils.parsing.command_parser import Parser, subparser, call_parse_result
from chatbot.bots.utils.parsing.common import rest_of_string
from chatbot.interface.messages import OutgoingMessage, IncomingMessage


class Luise:
    def __init__(self):
        self.name = "Luise"
        self.subs = []

        self.subcommands = self.collect_subcommands()
        for i in self.subcommands:
            i()
        self.parser: pyparsing.ParserElement = pyparsing.Or(self.subs)

    def create_msg(self, message, replying_to: IncomingMessage):
        return OutgoingMessage(channel=replying_to.channel, name=self.name, message=message,
                               delay=replying_to.delay + 1)

    def collect_subcommands(self):
        ret = []
        for v in dir(self):
            func = getattr(self, v)
            if hasattr(func, "_subparser"):
                ret.append(func)
        return ret

    def get_keyword(self):
        return pyparsing.CaselessKeyword(f"!{self.name}")

    async def react(self, msg: IncomingMessage):
        try:
            result = (self.get_keyword() + self.parser).parseString(msg.message)
        except pyparsing.ParseBaseException:
            return None

        return call_parse_result(result, msg)

    @subparser
    def help(self):
        def f(args, msg):
            return self.create_msg("Grade kann ich noch nicht so viel, nur was sagen und pongen, aber das wird sich "
                                   "noch ändern!\nIch habe euch alle ganz doll lieb! *knuuuuuuuuuuuuuudel*", msg)

        sub = Parser("help", func=f)
        self.subs.append(sub.as_pp_parser())

    @subparser
    def ping(self):
        def f(args, msg):
            return self.create_msg("pong", msg)

        sub = Parser("ping", func=f)
        self.subs.append(sub.as_pp_parser())

    @subparser
    def slap(self):
        def f(args, msg):
            return self.create_msg(f"{self.name} schlägt {args['target']}.", msg)

        sub = Parser("slap", func=f)
        sub.add_positional_argument("target", value_parser=rest_of_string)
        self.subs.append(sub.as_pp_parser())

    @subparser
    def hug(self):
        def f(args, msg):
            return self.create_msg(f"*knuddelt {args['target']}*", msg)

        sub = Parser("hug", func=f)
        sub.add_positional_argument("target")
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

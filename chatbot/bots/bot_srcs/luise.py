import pyparsing
import hashlib

from chatbot.bots.abc import BotABC
from chatbot.bots.utils.parsing.command_parser import Parser, subparser, call_parse_result
from chatbot.bots.utils.parsing.common import rest_of_string
from chatbot.interface.messages import OutgoingMessage, IncomingMessage
from chatbot import config


class Luise:
    def __init__(self):
        self.name = "Luise"

        self.subcommands = dict()
        self.collect_subcommands()
        self.parser: pyparsing.ParserElement = pyparsing.Or(self.subcommands.values())

    def create_msg(self, message, replying_to: IncomingMessage):
        return OutgoingMessage(channel=replying_to.channel, name=self.name, message=message,
                               delay=replying_to.delay + 1)

    def collect_subcommands(self):
        for v in dir(self):
            func = getattr(self, v)
            if hasattr(func, "_subparser"):
                self.subcommands[func] = None

        # So all are known beforehand
        for i in self.subcommands:
            self.subcommands[i] = i()
        return self.subcommands

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
        """ Ich sag dir, wie du mit mir umgehen sollst! """

        help_msg = f"Hallo, ich bin {self.name} und ich kann voooooooll tolle Sachen, zum Beispiel\n\n"
        help_msg += "\n".join(f"{v.command_word}:\t {k.__help__}" for k, v in self.subcommands.items())

        def f(args, msg):
            return self.create_msg(help_msg, msg)

        sub = Parser("help", func=f)
        return sub.as_pp_parser()

    @subparser
    def ping(self):
        """ Pong! """

        def f(args, msg):
            return self.create_msg("pong", msg)

        sub = Parser("ping", func=f)
        return sub.as_pp_parser()

    @subparser
    def slap(self):
        """ Ich schlage jemanden! -.- """

        def f(args, msg):
            return self.create_msg(f"*schlägt {args['target']}*", msg)

        sub = Parser("slap", func=f)
        sub.add_positional_argument("target", value_parser=rest_of_string)
        return sub.as_pp_parser()

    @subparser
    def hug(self):
        """ Ich knuddel jemanden! :-) """

        def f(args, msg):
            return self.create_msg(f"*knuddelt {args['target']}*", msg)

        sub = Parser("hug", func=f)
        sub.add_positional_argument("target", value_parser=rest_of_string)
        return sub.as_pp_parser()

    @subparser
    def say(self):
        """ Ich sage etwas! """

        def f(args, msg):
            return self.create_msg(args["rest"], msg)

        sub = Parser("say", func=f)
        sub.add_positional_argument("rest", value_parser=rest_of_string)

        return sub.as_pp_parser()

    def decide(self):
        """ Ich helfe dir, dich zu entscheiden! """
        salt = config["botmaster"]["luise"]["secret"].encode()

        def f(args, msg):
            res = hashlib.sha256(args["rest"].encode() + salt).digest()
            decision = '+' if int(res[0]) % 2 == 0 else '-'
            return self.create_msg(decision, msg)

        sub = Parser("decide", func=f)
        sub.add_positional_argument("rest", value_parser=rest_of_string)


BotABC.register(Luise)


def create_bot():
    return Luise()

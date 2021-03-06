from abc import abstractmethod, ABCMeta
from functools import wraps

import pyparsing
import pyparsing as pp
from pyparsing import ParseBaseException

from chatbot.interface.messages import OutgoingMessage, IncomingMessage
from .utils.parsing.command_parser import Parser


class BaseBot(metaclass=ABCMeta):
    def __init__(self):
        self.name = self.__class__.__name__
        self.react_on_bots = False

    def call_parse_result(self, res: pp.ParseResults, msg, *args, **kwargs):
        d = res.asDict()
        if "help" in d["options"]:
            return d["options"]["help"]
        return d["command"](msg, *args, bot=self, args=d["options"], **kwargs)

    def create_msg(self, msg, incoming):
        if msg is None:
            return None
        if isinstance(msg, OutgoingMessage):
            return msg
        elif isinstance(msg, str):
            return OutgoingMessage(message=msg, name=self.name, channel=incoming.channel, delay=incoming.delay + 1)
        elif isinstance(msg, dict):
            d = dict(channel=incoming.channel, delay=incoming.delay + 1, name=self.name)
            d.update(msg)
            return OutgoingMessage(**d)
        else:
            return [self.create_msg(i, incoming) for i in msg]

    async def react(self, msg: IncomingMessage):
        if not msg.bottag or self.react_on_bots:
            return self.create_msg(await self._react(msg), msg)
        return None

    async def shutdown(self):
        pass

    @abstractmethod
    async def _react(self, msg):
        pass


class CommandBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.subparser: pyparsing.ParserElement = pyparsing.Empty()
        self.reload_parsers()

    def reload_parsers(self):
        self.subparser: pyparsing.ParserElement = pyparsing.Or(map(Parser.as_pp_parser, self.commands.values()))

    async def _react(self, msg: IncomingMessage):
        try:
            result = (self.parser + self.subparser).parseString(msg.message)
        except ParseBaseException:
            return None

        return self.call_parse_result(result, msg)

    @property
    def parser(self):
        return pyparsing.CaselessKeyword(f"/{self.name}")

    @classmethod
    def add_command(cls, function, cmd):
        if not hasattr(cls, "commands"):
            cls.commands = dict()
        cls.commands[function] = cmd

    @classmethod
    def command(cls, *args, **kwargs):
        def decorator(f):
            name = kwargs.get("name", f.__name__)

            @wraps(f)
            def decorated(msg, *f_args, **f_kwargs):
                return f(*f_args, msg=msg, **f_kwargs)

            parser = Parser(name, func=decorated)
            for i in args:
                if isinstance(i, str):
                    parser.add_positional_argument(i)
                else:
                    parser.add_positional_argument(**i)

            for i in getattr(f, "__args__", []):
                parser.add_positional_argument(*i[0], **i[1])

            for k, v in kwargs.items():
                parser.add_optional_argument(**v)

            for i in getattr(f, "__opt_args__", []):
                parser.add_optional_argument(*i[0], **i[1])

            cls.add_command(decorated, parser)
            return decorated

        return decorator


def positional_argument(*args, **kwargs):
    def decorator(f):
        if not hasattr(f, "__args__"):
            setattr(f, "__args__", [])
        f.__args__.append((args, kwargs))
        return f

    return decorator


def optional_argument(*args, **kwargs):
    def decorator(f):
        if not hasattr(f, "__opt_args__"):
            setattr(f, "__opt_args__", [])
        f.__opt_args__.append((args, kwargs))
        return f

    return decorator

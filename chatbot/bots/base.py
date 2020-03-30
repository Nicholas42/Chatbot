from functools import wraps
from typing import Dict, Callable

from chatbot.bots.utils.parsing.command_parser import Parser
from chatbot.interface.messages import OutgoingMessage, IncomingMessage


class BaseBot:
    commands: Dict[Callable, Parser]

    def __init__(self):
        self.commands = dict()
        self.name = self.__class__.__name__
        self.react_on_bots = False

    def create_msg(self, msg, incoming):
        if isinstance(msg, OutgoingMessage):
            return msg
        elif isinstance(msg, str):
            return OutgoingMessage(message=msg, name=self.name, channel=incoming.channel, delay=incoming.delay + 1)
        else:
            d = dict(channel=incoming.channel, delay=incoming.delay + 1)
            d.update(msg)
            return OutgoingMessage(**d)

    async def react(self, msg: IncomingMessage):
        if not msg.bottag or self.react_on_bots:
            return await self._react(msg)
        return None

    async def shutdown(self):
        pass

    def command(self, *args, **kwargs):
        def decorator(f):
            name = kwargs.get("name", f.__name__)

            @wraps(f)
            def decorated(msg, *f_args, **f_kwargs):
                return self.create_msg(f(*f_args, msg=msg, bot=self, **f_kwargs), msg)

            parser = Parser(name, func=decorated)
            for i in args:
                if isinstance(i, str):
                    parser.add_positional_argument(i)
                else:
                    parser.add_positional_argument(**i)

            for k, v in kwargs.items():
                parser.add_optional_argument(**v)

            self.commands[decorated] = parser
            return decorated

        return decorator

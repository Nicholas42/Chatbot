from functools import wraps
from typing import Dict, Any, Callable

from chatbot.bots.utils.parsing.command_parser import Parser
from chatbot.interface.messages import OutgoingMessage


class BaseBot:
    commands: Dict[Callable, Parser]

    def __init__(self):
        self.commands = dict()
        self.name = self.__class__.__name__

    def create_msg(self, incoming, msg):
        if isinstance(msg, OutgoingMessage):
            return msg
        elif isinstance(msg, str):
            return OutgoingMessage(message=msg, name=self.name, channel=incoming.channel, delay=incoming.delay + 1)
        else:
            d = dict(channel=incoming.channel, delay=incoming.delay + 1)
            d.update(msg)
            return OutgoingMessage(**d)

    async def react(self, msg):
        return NotImplemented  # This should raise

    async def shutdown(self):
        pass

    def command(self, name, *args, **kwargs):
        def decorator(f):
            @wraps(f)
            def decorated(*f_args, **f_kwargs):
                return f(bot=self, *f_args, **f_kwargs)

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

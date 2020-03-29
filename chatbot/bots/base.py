from functools import wraps

from chatbot.bots.utils.parsing.command_parser import Parser


class BaseBot:

    def __init__(self):
        self.commands = dict()

    async def react(self, msg):
        return NotImplemented  # This should raise

    async def shutdown(self):
        pass

    def command(self, name, *args, **kwargs):
        def decorator(f):
            @wraps(f)
            def decorated(*f_args, **f_kwargs):
                return f(self, *f_args, **f_kwargs)

            parser = Parser(name, func=decorated)
            for i in args:
                if isinstance(i, str):
                    parser.add_positional_argument(i)
                else:
                    parser.add_positional_argument(**i)

            for k, v in kwargs.items():
                parser.add_optional_argument(**v)

            self.commands[name] = parser
            return decorated

        return decorator

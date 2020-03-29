from typing import Optional, Callable

import pyparsing as pp

from chatbot.bots.utils.parsing.common import intersperse_parser, update_dict, rest_of_string
from .common import common_parsers


def subparser(f):
    f._subparser = True
    return f


def call_parse_result(res: pp.ParseResults, msg, *args, **kwargs):
    d = res.asDict()
    return d["command"](msg, *args, args=d["options"], **kwargs)


class Parser:

    def __init__(self, command_word: str, func: Optional[Callable] = None):
        self.command_word = command_word
        self.opt_args = []
        self.pos_args = []
        self.func = func

    def add_optional_argument(self, name_list: list, result_type: Callable = bool, arg_name: Optional[str] = None,
                              value_parser: Optional[pp.ParserElement] = None, action: Optional[Callable] = None):
        if arg_name is None:
            arg_name = name_list[0]

        arg = pp.MatchFirst([pp.CaselessKeyword(i) for i in name_list]).setParseAction(lambda x: arg_name)

        if value_parser is None:
            value_parser = common_parsers[result_type]
        if action is not None:
            value_parser.addParseAction(action)

        # It is important that the ParseAction is inside the Optional! Otherwise we will get errors if it does not
        # match.
        complete = (arg + value_parser.copy()).setName(arg_name).setParseAction(lambda x: {x[0]: x[1]})
        self.opt_args.append(pp.Optional(complete(arg_name)))

    def add_positional_argument(self, name: str, result_type: Callable = str,
                                value_parser: Optional[pp.ParserElement] = None, action: Optional[Callable] = None):
        if value_parser is None:
            value_parser = common_parsers[result_type]
        value_parser = value_parser(name).setName(name).addParseAction(action if action else lambda x: {name: x[0]})

        self.pos_args.append(value_parser)

    def as_pp_parser(self) -> pp.ParserElement:
        pos_args = self.pos_args + [rest_of_string("_rest").setName("_rest").addParseAction(lambda x: {"_rest": x[0]})]
        if self.opt_args:
            optionals = pp.Or(self.opt_args)
            args = intersperse_parser(pos_args, optionals)
        else:
            args = pp.And(pos_args)
        args.setParseAction(update_dict)
        cw = pp.CaselessKeyword(self.command_word)("command").setParseAction(lambda x: self.func)

        return (cw + args("options")).streamline()

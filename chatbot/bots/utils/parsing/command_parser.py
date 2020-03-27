from typing import Optional, Callable

import pyparsing as pp

from chatbot.bots.utils.parsing.common import intersperse_parser, update_dict
from .common import common_parsers


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
            value_parser = common_parsers[result_type].copy()
        if action is not None:
            value_parser.addParseAction(action)

        self.opt_args.append(pp.Optional(arg + value_parser).setParseAction(lambda x: {x[0]: x[1]}))

    def add_positional_argument(self, name: str, result_type: Callable = str,
                                value_parser: Optional[pp.ParserElement] = None, action: Optional[Callable] = None):
        if value_parser is None:
            value_parser = common_parsers[result_type].copy()
        value_parser.addParseAction(action if action else lambda x: {name: x[0]})

        self.pos_args.append(value_parser)

    def as_pp_parser(self) -> pp.ParserElement:
        optionals = pp.Or(self.opt_args)
        args = intersperse_parser(self.pos_args, optionals).setParseAction(update_dict)
        if self.func is not None:
            args.addParseAction(self.func)

        return pp.CaselessKeyword(self.command_word) + args

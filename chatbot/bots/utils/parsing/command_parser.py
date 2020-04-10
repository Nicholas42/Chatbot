from collections import namedtuple
from typing import Optional, Callable

import pyparsing as pp

from .common import intersperse_parser, update_dict, common_parsers, rest_parser, default_parser


class Parser:
    _arg_info = namedtuple("_arg_info", ("pp_parser", "name", "aliases", "help"))

    def __init__(self, command_word: str, func: Optional[Callable] = None, add_help=True, help_prefix=None):
        self.command_word = command_word
        self.func = func
        self.add_help = add_help
        self.help_prefix = help_prefix

        self.opt_args = []
        self.pos_args = []

        self.help_arg = self._create_optional_argument(["--help", "-h"], "help", default_parser(self.get_help),
                                                       "Zeigt diese Hilfe an.", optional=False)

    def add_optional_argument(self, name_list: list, result_type: Callable = bool, arg_name: Optional[str] = None,
                              value_parser: Optional[pp.ParserElement] = None, action: Optional[Callable] = None,
                              help_text=None):
        if arg_name is None:
            arg_name = name_list[0]

        if value_parser is None:
            value_parser = common_parsers[result_type]
        if action is not None:
            value_parser.addParseAction(action)

        self.opt_args.append(self._create_optional_argument(name_list, arg_name, value_parser, help_text))

    def _create_optional_argument(self, name_list: list, arg_name: str, value_parser: pp.ParserElement, help_text=None,
                                  optional=True):

        arg = pp.MatchFirst([pp.CaselessKeyword(i) for i in name_list]).setParseAction(lambda x: arg_name)

        # It is important that the ParseAction is inside the Optional! Otherwise we will get errors if it does not
        # match.
        complete = (arg + value_parser.copy()).setName(arg_name).setParseAction(lambda x: {x[0]: x[1]})(arg_name)
        if optional:
            complete = pp.Optional(complete)
        return self._arg_info(complete, arg_name, name_list, help_text)

    def add_positional_argument(self, name: str, result_type: Callable = str, help_text=None,
                                value_parser: Optional[pp.ParserElement] = None, action: Optional[Callable] = None):
        if value_parser is None:
            value_parser = common_parsers[result_type]
        value_parser = value_parser(name).setName(name).addParseAction(action if action else lambda x: {name: x[0]})

        self.pos_args.append(self._arg_info(value_parser, name, [name], help_text))

    def get_full_opts(self):
        ret = self.opt_args[:]
        if self.add_help:
            ret.append(self.help_arg)
        return ret

    def get_usage(self):
        prefix = f"{self.help_prefix} " if self.help_prefix else ""
        pos = " ".join(i.name for i in self.pos_args)
        opt = " ".join(f"[{i.name}]" for i in self.get_full_opts())
        return f"{prefix}{self.command_word} {pos} {opt}"

    @staticmethod
    def _format_args(args, name):
        if not args:
            return []

        ret = ["", name]
        for i in args:
            aliases = " | ".join(i.aliases)
            ret.append(f"\t{aliases}\t\t{i.help}")

        return ret

    def get_help(self):
        ret = [self.get_usage()]
        ret += self._format_args(self.pos_args, "Parameter:")
        ret += self._format_args(self.get_full_opts(), "Optionale Parameter:")

        return '\n'.join(ret)

    def as_pp_parser(self) -> pp.ParserElement:
        pos_args = [i.pp_parser for i in self.pos_args] + [rest_parser.copy()]
        opt_args = [i.pp_parser for i in self.opt_args]
        if opt_args:
            optionals = pp.Or(opt_args)
            args = intersperse_parser(pos_args, optionals)
        else:
            args = pp.And(pos_args)
        args.setParseAction(update_dict)
        cw = pp.CaselessKeyword(self.command_word)("command").setParseAction(lambda x: self.func)

        if self.add_help:
            args = (self.help_arg.pp_parser | args).setParseAction(lambda x: x[0])

        return (cw + args("options")).streamline()

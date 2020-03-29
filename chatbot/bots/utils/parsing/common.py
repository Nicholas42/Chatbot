import pyparsing as pp
from pyparsing import pyparsing_common as ppc

WHITE_CHARS = pp.ParserElement.DEFAULT_WHITE_CHARS
uword = pp.Suppress(pp.SkipTo(pp.WordStart())) + pp.CharsNotIn(WHITE_CHARS)

common_parsers = {
    int: pp.Combine(pp.Optional('-') + pp.Word(pp.nums)).setParseAction(ppc.convertToInteger) + pp.Suppress(
        pp.WordEnd()),
    str: (pp.QuotedString("'") | pp.QuotedString('"') | uword) + pp.Suppress(pp.WordEnd()),
    bool: pp.Empty().setParseAction(lambda x: True)
}

rest_of_line = pp.restOfLine.copy()
rest_of_string = pp.SkipTo(pp.StringEnd())


def update_dict(dict_list):
    ret = dict()
    for i in dict_list:
        for k, v in i.items():
            ret[k] = v
    return ret


def intersperse_parser(parser_list: list, interspersed: pp.ParserElement) -> pp.ParserElement:
    ret = interspersed.copy()
    for i in parser_list:
        ret = ret + i.copy() + interspersed.copy()

    return ret

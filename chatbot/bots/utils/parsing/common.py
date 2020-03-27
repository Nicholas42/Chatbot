import pyparsing as pp
from pyparsing import pyparsing_common as ppc
from pyparsing import pyparsing_unicode as ppu

uword = pp.Word(ppu.printables)

common_parsers = {
    int: pp.Combine(pp.Optional('-') + pp.Word(pp.nums)).setParseAction(ppc.convertToInteger) + pp.Suppress(
        pp.WordEnd()),
    str: (pp.QuotedString("'") | pp.QuotedString('"') | uword) + pp.Suppress(pp.WordEnd()),
    bool: pp.Empty().setParseAction(lambda x: True)
}


def update_dict(dict_list, update_func=lambda old, new: new):
    ret = dict()
    for i in dict_list:
        for k, v in i.items():
            if k in ret:
                ret[k] = update_func(ret[k], v)
            else:
                ret[k] = v
    return ret


def intersperse_parser(parser_list: list, interspersed: pp.ParserElement) -> pp.ParserElement:
    ret = interspersed
    for i in parser_list:
        ret = ret + i

    return ret

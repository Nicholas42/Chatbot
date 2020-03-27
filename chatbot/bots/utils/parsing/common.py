import pyparsing as pp
from pyparsing import pyparsing_common as ppc

quoted_string = pp.dblQuotedString | pp.sglQuotedString

common_parsers = {
    int: pp.Word(pp.nums, asKeyword=True).setParseAction(ppc.convertToInteger),
    str: quoted_string,
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

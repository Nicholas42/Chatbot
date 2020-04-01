import pyparsing as pp

scheme = pp.Literal("http") + pp.Optional('s') + "://"
url = pp.Optional("www.") + "youtube." + ... + (pp.Literal("/v/") ^ "&v=" ^ "?v=" ^ "/embed/")
short = pp.Literal("youtu.be/")
vid = pp.SkipTo(pp.LineEnd() ^ pp.Char("#?&") ^ pp.White())("vid")

parser = pp.Suppress(pp.Optional(scheme) + (url ^ short)) + vid


def get_vid(s):
    return parser.parseString(s).asDict()["vid"]

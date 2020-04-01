from unittest import TestCase

from chatbot.bots.utils.parsing.command_parser import Parser
from chatbot.bots.utils.parsing.youtube import get_vid, parser as yt_parser

_tests = """ http://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index
            http://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0
            http://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s
            http://www.youtube.com/embed/0zM3nApSvMg?rel=0
            http://www.youtube.com/watch?v=0zM3nApSvMg
            http://youtu.be/0zM3nApSvMg""".split()

_vid = "0zM3nApSvMg"


class TestYT(TestCase):
    def test_parse(self):

        for i in _tests:
            self.assertEqual(get_vid(i), _vid)

    def test_full_parser(self):
        parser = Parser("sing")
        parser.add_optional_argument(["--learn"], value_parser=yt_parser, arg_name="learn")
        pp = parser.as_pp_parser()

        for i in _tests:
            res = pp.parseString(f"sing --learn {i} --learn {i}").asDict()["options"]
            self.assertEqual(res["learn"], _vid)

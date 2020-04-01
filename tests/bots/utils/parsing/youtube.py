from unittest import TestCase

from chatbot.bots.utils.parsing.youtube import get_vid


class TestYT(TestCase):
    def test_parse(self):
        vid = "0zM3nApSvMg"
        tests = """ http://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index
                    http://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0
                    http://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s
                    http://www.youtube.com/embed/0zM3nApSvMg?rel=0
                    http://www.youtube.com/watch?v=0zM3nApSvMg
                    http://youtu.be/0zM3nApSvMg""".split()

        for i in tests:
            self.assertEqual(get_vid(i), vid)

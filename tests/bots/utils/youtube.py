from unittest import TestCase

from chatbot.bots.utils.youtube import get_video_info


class TestYT(TestCase):

    def test_get_info(self):
        get_video_info("ytWz0qVvBZ0")

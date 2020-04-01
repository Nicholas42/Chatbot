from unittest import TestCase

from chatbot import glob

glob.configure()
from chatbot.bots.utils.youtube import get_video_info


class TestYT(TestCase):

    def test_get_info(self):
        print(get_video_info("ytWz0qVvBZ0"))

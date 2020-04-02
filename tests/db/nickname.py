from unittest import TestCase

from chatbot import glob
from chatbot.database.db import DB
from chatbot.database.nickname import get_user


class TestNickname(TestCase):
    glob.configure()
    db = DB()

    def setUp(self) -> None:
        self.session = self.db.session

    def tearDown(self) -> None:
        self.session.rollback()

    def test_get_user(self):
        nicholas = get_user("        nIchoLasSchwAB")
        self.assertEqual(nicholas.user_id, 412)

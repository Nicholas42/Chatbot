from chatbot.config import Config
from unittest import TestCase
from pathlib import Path
from os import environ


class TestConfig(TestCase):
    def setUp(self) -> None:
        for i in environ:
            del environ[i]
        test_data = Path(__file__).parent / "test_data"
        self.config = Config(test_data / "configurations", test_data / "env-file")

    def test_normal(self):
        self.assertEqual(self.config["connection"]["path"], "/websocket")

    def test_hidden(self):
        self.assertEqual(self.config["user"]["username"], "Testy")
        self.assertEqual(self.config["user"]["password"], "Safe")
        self.assertEqual(self.config["user"]["stuff"], {"secret": "VERY SECRET", "not secret": None})

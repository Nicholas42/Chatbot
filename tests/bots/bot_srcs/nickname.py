from unittest import TestCase

from chatbot import glob
from chatbot.bots.bot_srcs.nickname import Nickname
from chatbot.database.nickname import QEDler


class TestNickname(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nickname = Nickname()

    def test_parser(self):
        tests = [("!nickname nicholas", {"name": "nicholas"}),
                 ("!nickname 'Santa Claus' -a Weihnachtsmann", {"name": "Santa Claus", "add": "Weihnachtsmann"}),
                 ("!nickname 'Knecht Ruprecht' -r \"Santa's Little Helper\"",
                  {"name": "Knecht Ruprecht", "remove": "Santa's Little Helper"})]

        for i in tests:
            i[1].update({"_rest": ""})
            self.assertEqual(self.nickname.parser.parseString(i[0])["options"], i[1])

    def test_db(self):
        glob.configure()

        nicholas: QEDler = glob.db.session.query(QEDler).filter(QEDler.user_id == 412).one()

        show = self.nickname.work(None, {"name": "epsilon"})
        self.assertEqual(len(show.split('\n')), len(nicholas.nicknames) + 1)

        add = self.nickname.work(None, {"name": "epsilon", "add": "   NichOlas"})

        self.assertEqual(add, "NicholasSchwab hat jetzt den Nickname NichOlas.")

        remove = self.nickname.work(None, {"name": "epsilon", "remove": "nicholas"})

        self.assertEqual(len(nicholas.nicknames), 1)

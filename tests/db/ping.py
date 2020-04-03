from unittest import TestCase

from chatbot import glob
from chatbot.database.nickname import QEDler, Nickname, create_nickname
from chatbot.database.ping import Ping


class TestPing(TestCase):
    glob.configure()

    def test_user(self):
        p = Ping(user_id=412, message="Blub", sender="Your Mom")
        with glob.db.context as session:
            session.add(p)
            nicholas = session.query(QEDler).filter(QEDler.user_id == 412).one()

            nicholas.pings.append(p)

            self.assertTrue(p in nicholas.pings)
            session.add(create_nickname("Schatzi"))

            nick = session.query(Nickname).filter(Nickname.nickname == "schAtzi   ").one()

            p.target = nick._column_id

            self.assertTrue(p in nick.pings)

            session.rollback()

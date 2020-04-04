from unittest import TestCase

from chatbot.database.db import database
from chatbot.database.nickname import QEDler, Nickname, create_nickname, get_user
from chatbot.database.ping import Ping, get_pings


class TestPing(TestCase):
    session = None

    def setUp(self) -> None:
        self.session = database.session

    def tearDown(self) -> None:
        self.session.rollback()
        self.session.close()

    def test_get_pings(self):
        p = Ping(user_id=412, message="Blub", sender="Your Mom")
        self.session.add(p)

        self.assertEqual(get_user(self.session, "EpsiLon").user_id, 412)
        self.assertIn(p, get_pings(self.session, "EpsiLon"))
        self.assertIn(p, get_pings(self.session, "NicholasSchwab"))

        self.session.rollback()

    def test_user(self):
        p = Ping(user_id=412, message="Blub", sender="Your Mom")
        self.session.add(p)
        nicholas = self.session.query(QEDler).filter(QEDler.user_id == 412).one()

        nicholas.pings.append(p)

        self.assertTrue(p in nicholas.pings)
        self.session.add(create_nickname("Schatzi"))

        nick = self.session.query(Nickname).filter(Nickname.nickname == "schAtzi   ").one()

        p.target = nick

        self.assertTrue(p in nick.pings)
        self.assertTrue(p.is_active)
        self.assertTrue(p in self.session.query(Ping).filter(Ping.is_active).all())
        self.assertTrue(p in self.session.query(Ping).filter(Ping.target == nick).filter(Ping.is_active).all())
        self.assertTrue(p in filter(lambda x: x.is_active, nick.pings))

        self.session.rollback()

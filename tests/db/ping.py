from unittest import TestCase

from chatbot import glob
from chatbot.database.nickname import QEDler, Nickname, create_nickname, get_user
from chatbot.database.ping import Ping, get_pings


class TestPing(TestCase):
    glob.configure()

    def test_get_pings(self):
        with glob.db.context as session:
            p = Ping(user_id=412, message="Blub", sender="Your Mom")
            session.add(p)

            self.assertEqual(get_user(session, "EpsiLon").user_id, 412)
            self.assertIn(p, get_pings(session, "EpsiLon"))
            self.assertIn(p, get_pings(session, "NicholasSchwab"))

            session.rollback()

    def test_user(self):
        p = Ping(user_id=412, message="Blub", sender="Your Mom")
        with glob.db.context as session:
            session.add(p)
            nicholas = session.query(QEDler).filter(QEDler.user_id == 412).one()

            nicholas.pings.append(p)

            self.assertTrue(p in nicholas.pings)
            session.add(create_nickname("Schatzi"))

            nick = session.query(Nickname).filter(Nickname.nickname == "schAtzi   ").one()

            p.target = nick

            self.assertTrue(p in nick.pings)
            self.assertTrue(p.is_active)
            self.assertTrue(p in session.query(Ping).filter(Ping.is_active).all())
            self.assertTrue(p in session.query(Ping).filter(Ping.target == nick).filter(Ping.is_active).all())
            self.assertTrue(p in filter(lambda x: x.is_active, nick.pings))

            session.rollback()

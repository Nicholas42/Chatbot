from pyparsing import ParseException

from chatbot.bots.base import BaseBot
from chatbot.bots.utils.formatting import format_date
from chatbot.bots.utils.parsing.command_parser import Parser
from chatbot.config import config
from chatbot.database.nickname import get_user, create_nickname, Nickname
from chatbot.database.ping import Ping as PingModell, get_pings
from chatbot.database.utils import inject_session
from chatbot.interface.messages import IncomingMessage


def _format_pings(pings):
    ret = []
    i: PingModell
    for i in pings:
        v = f" (verifiziert als {i.verified})" if i.verified else ""
        ret.append(f"{i.sender} sagte am {format_date(i.ping_time)}{v}:")
        for line in i.message.split('\n'):
            ret.append(f"> {line}")

    return '\n'.join(ret)


class Ping(BaseBot):
    def __init__(self):
        super().__init__()

        _parser = Parser(f"/{self.name}", self.work)
        _parser.add_positional_argument("target")

        self.parser = _parser.as_pp_parser()
        self.id_diff = config["botmaster"]["ping"]["diff"]

    @inject_session
    def work(self, msg: IncomingMessage, args, session):
        target = get_user(session, args["target"])
        if target is None:
            target = create_nickname(args["target"])
            session.add(target)

        ping = PingModell(post_id=msg.id, message=args["_rest"], ping_time=msg.date, sender=msg.name,
                          verified=msg.username)
        session.add(ping)

        if isinstance(target, Nickname):
            ping.target = target
        ping.user_id = target.user_id

    @inject_session
    def pong(self, msg: IncomingMessage, session):
        pings = get_pings(session, msg.name, msg.user_id)
        if not pings:
            return

        in_order = sorted(pings, key=lambda x: x.send_time)
        if not any(map(lambda x: x.post_id - msg.id > self.id_diff, in_order)):
            return

        intro = f"{msg.name.strip()}, dir wollte jemand etwas sagen:"
        return intro + _format_pings(in_order)

    async def _react(self, incoming):
        try:
            result = self.parser.parseString(incoming.message)
            self.call_parse_result(result, incoming)
            return self.pong(incoming)
        except ParseException:
            return None

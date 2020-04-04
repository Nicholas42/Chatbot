from datetime import timedelta, datetime, timezone

from dateutil.parser import ParserError
from pyparsing import ParserElement, ParseException

from chatbot import glob
from chatbot.bots.base import BaseBot
from chatbot.bots.utils.formatting import format_date
from chatbot.bots.utils.parsing.command_parser import Parser
from chatbot.bots.utils.parsing.common import rest_of_string
from chatbot.bots.utils.parsing.date import parse_date
from chatbot.database.messages import OutgoingMessageModel
from chatbot.interface.messages import OutgoingMessage, IncomingMessage
from chatbot.utils.async_sched import AsyncScheduler


class ReminderSender:
    def __init__(self, slack=timedelta(minutes=2)):
        self.slack = slack
        self.sched = AsyncScheduler(0, self._send)
        self.reschedule()

    def schedule(self, msg: OutgoingMessage, send_time: datetime):
        model = OutgoingMessageModel.construct(msg, send_time=send_time, sent=False)

        with glob.db.context as session:
            session.add(model)

        self.reschedule()

    def reschedule(self):
        next_time = self.get_next_time()
        if next_time is not None:
            self.sched.reset(next_time)
            return True
        return False

    @staticmethod
    def get_next_time() -> datetime:
        with glob.db.context as session:
            return session.query(OutgoingMessageModel.send_time).order_by(OutgoingMessageModel.send_time).filter(
                OutgoingMessageModel.still_to_send()).limit(1).scalar()

    def _send(self):
        limit = datetime.now(timezone.utc) + self.slack
        with glob.db.context as session:
            to_send = session.query(OutgoingMessageModel).filter(OutgoingMessageModel.still_to_send()).filter(
                OutgoingMessageModel.send_time < limit).all()
            messages = []

            for i in to_send:
                messages.append(i.convert())
                session.delete(i)

        for i in messages:
            glob.bridge.put_outgoing_nowait(i)

        self.reschedule()


class ReminderBot(BaseBot):
    def __init__(self):
        super().__init__()

        self.scheduler = ReminderSender()
        _parser = Parser("!remind", self.work)
        _parser.add_optional_argument(["-t", "--target"], result_type=str, arg_name="target")
        _parser.add_positional_argument("date")
        _parser.add_positional_argument("msg", value_parser=rest_of_string)

        self.parser: ParserElement = _parser.as_pp_parser()

    def work(self, msg: IncomingMessage, args):
        target = args.get("target", msg.name.strip())
        try:
            date = parse_date(args["date"])
        except ParserError:
            date = None
        except OverflowError:
            return f"Das Datum ist zu groß..."

        if date is None:
            return f"Ich konnte das Datum nicht lesen :-("

        outgoing = f"!ping '{target}' Du wolltest an folgendes erinnert werden:\n{args['msg']}"
        self.scheduler.schedule(self.create_msg({"message": outgoing, "bottag": 0}, msg), date)

        return f"Eine Nachricht wurde für {target} zum Zeitpunkt {format_date(date)} eingeplant."

    async def _react(self, incoming):
        try:
            result = self.parser.parseString(incoming.message)
            return self.call_parse_result(result, incoming)
        except ParseException:
            return None


def create_bot(*args, **kwargs):
    return ReminderBot()

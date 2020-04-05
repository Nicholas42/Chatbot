from pyparsing import ParseBaseException

from chatbot.bots.base import BaseBot
from chatbot.bots.utils.parsing.command_parser import Parser
from chatbot.database.nickname import get_user, QEDler, Nickname as NicknameModel
from chatbot.database.utils import normalize_nickname, inject_session


def _add_nick(session, existing: QEDler, to_add):
    normalized = normalize_nickname(to_add)
    if normalized == "":
        return f"Der Nickname darf nicht leer sein."
    user = get_user(session, normalized)
    if user is not None:
        if isinstance(user, QEDler):
            return f"{to_add.strip()} ist der Name eines QEDlers."
        elif user.qedler is not None:
            return f"{user.qedler.user_name} heißt schon so."
        else:
            session.merge(user).user_id = existing.user_id
    else:
        new = NicknameModel(nickname=to_add, original=to_add, user_id=existing.user_id)
        session.add(new)

    return f"{existing.user_name} hat jetzt den Nickname {to_add.strip()}."


def _remove_nick(session, existing: QEDler, to_remove):
    normalized = normalize_nickname(to_remove)
    if normalized not in existing.nicknames:
        return f"{existing.user_name} hat den Nickname {to_remove.strip()} nicht."

    copy = session.merge(existing)
    copy.nicknames.remove(normalized)

    return f"{existing.user_name} hat jetzt den Nickname {to_remove.strip()} nicht mehr."


def _show_nicks(existing: QEDler):
    intro = f"{existing.user_name} hat die Nicknames:\n"
    return intro + "\n".join(f"{i.original}" for i in existing.nickname_objects)


class Nickname(BaseBot):
    def __init__(self):
        super().__init__()

        _parser = Parser("/nickname", self.work)

        _parser.add_positional_argument("name")
        _parser.add_optional_argument(["-a", "--add"], result_type=str, arg_name="add")
        _parser.add_optional_argument(["-r", "--remove"], result_type=str, arg_name="remove")

        self.parser = _parser.as_pp_parser()

    @inject_session
    def work(self, msg, args, session, **__):

        qedler = get_user(session, args["name"])
        if qedler is None:
            return f"Ich kenne {args['name']} nicht."
        if isinstance(qedler, NicknameModel):
            qedler = qedler.qedler
        if "add" in args:
            return _add_nick(session, qedler, args["add"])
        if "remove" in args:
            return _remove_nick(session, qedler, args["remove"])

        return _show_nicks(qedler)

    async def _react(self, msg):
        try:
            res = self.parser.parseString(msg.message)
        except ParseBaseException:
            return None

        return self.call_parse_result(res, msg)


def create_bot(*_, **__):
    return Nickname()

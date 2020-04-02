import hashlib
import random

import pyparsing
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from chatbot import glob
from chatbot.bots.base import BaseBot, optional_argument
from chatbot.bots.utils.parsing.command_parser import Parser, call_parse_result
from chatbot.bots.utils.parsing.common import uword
from chatbot.bots.utils.parsing.youtube import parser as yt_parser
from chatbot.bots.utils.youtube import get_video_info, VideoNotFoundError, check_restriction
from chatbot.database.songs import Song
from chatbot.interface.messages import IncomingMessage
from chatbot.utils.async_sched import AsyncScheduler


def _lalala():
    length = random.randint(8, 14)
    return "la" + "a".join(random.choices(["l", "ll"], weights=[5, 1], k=length)) + "a"


class Luise(BaseBot):
    _time_out = 900  # seconds until luise renames herself back

    def __init__(self, botmaster, config=None):
        super().__init__()
        if config is None:
            config = glob.config
        self.config = config["botmaster"]["default_bots"]["luise"]

        self.parser: pyparsing.ParserElement = pyparsing.Empty()
        self.botmaster = None
        self.rename_msg = None
        self.timer = AsyncScheduler(self._time_out, self._rename)

    def _rename(self):
        self.name = self.__class__.__name__
        self.botmaster.bridge.put_outgoing_nowait(self.create_msg("I am back! :-)", self.rename_msg))

    def reset_rename(self, message):
        if self.__class__.__name__ != self.name:
            self.rename_msg = message
            self.timer.reset(self._time_out)

    def reload_parsers(self):
        self.parser: pyparsing.ParserElement = pyparsing.Or(map(Parser.as_pp_parser, self.commands.values()))

    def get_keyword(self):
        return pyparsing.CaselessKeyword(f"!{self.name}")

    async def _react(self, msg: IncomingMessage):
        try:
            result = (self.get_keyword() + self.parser).parseString(msg.message)
        except pyparsing.ParseBaseException as e:
            return None

        self.reset_rename(msg)

        return call_parse_result(result, msg)


@Luise.command()
def help(bot: Luise, **kwargs):
    """ Ich sag dir, wie du mit mir umgehen sollst! """

    help_msg = f"Hallo, ich bin {bot.name} und ich kann voooooooll tolle Sachen, zum Beispiel\n\n"
    return help_msg + "\n".join(f"{v.command_word}:\n\t {k.__doc__}" for k, v in bot.commands.items())


@Luise.command({"name": "new_name", "value_parser": uword})
def be(bot, args, msg, **kwargs):
    """ Ich verwandel mich in jemand anderen! """
    bot.name = args["new_name"]
    bot.reset_rename(msg)

    return _lalala()


@Luise.command()
def ping(**kwargs):
    """ Pong! """

    return "pong"


@Luise.command()
def slap(args, **kwargs):
    """ Ich schlage jemanden! -.- """

    return f"*schlägt {args['_rest']}*"


@Luise.command()
def hug(args, **kwargs):
    """ Ich knuddel jemanden! :-) """

    return f"*knuddelt {args['_rest']}*"


@Luise.command()
def say(args, **kwargs):
    """ Ich sage etwas! """

    return args["_rest"]


@Luise.command()
def decide(bot, args, **kwargs):
    """ Ich helfe dir, dich zu entscheiden! """
    salt = bot.config["secret"].encode()

    res = hashlib.sha256(args["_rest"].encode() + salt).digest()
    return '+' if int(res[0]) % 2 == 0 else '-'


@Luise.command()
def featurerequest(args, **kwargs):
    """ Ich wünsch mir was! Und wenn ich gaaaaanz fest dran glaube wird es auch Wirklichkeit!"""

    return f"Ich will {args['_rest']}!"


@Luise.command()
@optional_argument(name_list=["-a", "-l", "--add", "--learn"], value_parser=yt_parser, arg_name="learn")
@optional_argument(name_list=["-r", "--remove"], value_parser=yt_parser, arg_name="remove")
def sing(args, **kwargs):
    """ Ich singe was für dich! """
    if "learn" in args:
        to_learn = args["learn"]

        with glob.db.context as session:
            song = session.query(Song).filter(Song.video_id == to_learn).one_or_none()
            if song is not None:
                return f"Ich kann {song.title} schon singen!"
        try:
            info = get_video_info(to_learn)
        except (VideoNotFoundError, ConnectionRefusedError) as e:
            return str(e)

        if not check_restriction(info):
            return f"Video mit der ID {to_learn} ist in Deutschland nicht ansehbar."
        model = Song(video_id=to_learn, title=info["title"])

        with glob.db.context as session:
            session.add(model)

        return f"Ich kann jetzt {info['title']} singen!"

    elif "remove" in args:
        to_remove = args["remove"]
        with glob.db.context as session:
            try:
                song = session.query(Song).filter_by(Song.video_id == to_remove).one()
            except NoResultFound:
                return f"Ich kann das gar nicht singen!"
            except MultipleResultsFound:
                return f"Irgendwas ist sehr schief gegangen /o\\"
            title = song.title
            session.delete(song)
        return f"Ich kann jetzt {title} nicht mehr singen!"
    else:
        with glob.db.context as session:
            song: Song = random.sample(session.query(Song).all(), 1)[0]
            return f"{song.title}\n{song.url}"


def create_bot(botmaster):
    luise = Luise(botmaster)
    luise.reload_parsers()
    return luise

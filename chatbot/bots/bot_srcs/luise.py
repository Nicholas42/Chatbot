import hashlib
import random

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from chatbot.config import config
from chatbot.database.db import database
from chatbot.database.songs import Song
from chatbot.interface.messages import IncomingMessage
from chatbot.utils.async_sched import AsyncScheduler
from ..base import optional_argument, CommandBot
from ..utils.parsing.common import uword
from ..utils.parsing.youtube import parser as yt_parser
from ..utils.youtube import get_video_info, VideoNotFoundError, check_restriction


def _lalala():
    length = random.randint(8, 14)
    return "la" + "a".join(random.choices(["l", "ll"], weights=[5, 1], k=length)) + "a"


class Luise(CommandBot):
    _time_out = 900  # seconds until luise renames herself back

    def __init__(self, botmaster, _config=None):
        super().__init__()
        if _config is None:
            _config = config
        self.config = _config["botmaster"]["default_bots"]["luise"]

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

    async def _react(self, msg: IncomingMessage):
        result = await super()._react(msg)

        if result is not None:
            self.reset_rename(msg)

        return result


@Luise.command()
def help(bot: Luise, **__):
    """ Ich sag dir, wie du mit mir umgehen sollst! """

    help_msg = f"Hallo, ich bin {bot.name} und ich kann voooooooll tolle Sachen, zum Beispiel\n\n"
    return help_msg + "\n".join(f"{v.command_word}:\n\t {k.__doc__}" for k, v in bot.commands.items())


@Luise.command({"name": "new_name", "value_parser": uword})
def be(bot, args, msg, **__):
    """ Ich verwandel mich in jemand anderen! """
    bot.name = args["new_name"]
    bot.reset_rename(msg)

    return _lalala()


@Luise.command()
def ping(**__):
    """ Pong! """

    return "pong"


@Luise.command()
def slap(args, **__):
    """ Ich schlage jemanden! -.- """

    return f"*schlägt {args['_rest']}*"


@Luise.command()
def hug(args, **__):
    """ Ich knuddel jemanden! :-) """

    return f"*knuddelt {args['_rest']}*"


@Luise.command()
def say(args, **__):
    """ Ich sage etwas! """

    return args["_rest"]


@Luise.command()
def decide(bot, args, **__):
    """ Ich helfe dir, dich zu entscheiden! """
    salt = bot.config["secret"].encode()

    res = hashlib.sha256(args["_rest"].encode() + salt).digest()
    return '+' if int(res[0]) % 2 == 0 else '-'


@Luise.command()
def featurerequest(args, **__):
    """ Ich wünsch mir was! Und wenn ich gaaaaanz fest dran glaube wird es auch Wirklichkeit!"""

    return f"Ich will {args['_rest']}!"


@Luise.command()
@optional_argument(name_list=["-a", "-l", "--add", "--learn"], value_parser=yt_parser, arg_name="learn")
@optional_argument(name_list=["-r", "--remove"], value_parser=yt_parser, arg_name="remove")
def sing(args, **__):
    """ Ich singe was für dich! """
    if "learn" in args:
        to_learn = args["learn"]

        with database.context as session:
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

        with database.context as session:
            session.add(model)

        return f"Ich kann jetzt {info['title']} singen!"

    elif "remove" in args:
        to_remove = args["remove"]
        with database.context as session:
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
        with database.context as session:
            song: Song = random.sample(session.query(Song).all(), 1)[0]
            return f"{song.title}\n{song.url}"


def create_bot(botmaster):
    return Luise(botmaster)

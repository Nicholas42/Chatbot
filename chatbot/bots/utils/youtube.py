from requests import Session

from chatbot import glob
from chatbot.database.songs import Song


class VideoNotFoundError(LookupError):
    pass


def check_restriction(restriction):
    if "DE" in restriction.get("disallowed", []):
        return False

    allowed = restriction.get("allowed", [])
    if allowed and "DE" not in allowed:
        return False

    return True


def get_video_info(vid, searched=None):
    if searched is None:
        searched = dict(title=("snippet", "title"), restriction=("contentDetails", "regionRestriction"))
    info = lookup_video(vid, map(lambda x: x[0], searched.values()))
    ret = {}
    for k, v in searched.items():
        val = info
        for i in v:
            val = val[i]

        ret[k] = val

    return ret


def lookup_video(vid, parts=("snippet", "contentDetail")):
    _BASE_URL = "https://www.googleapis.com/youtube/v3/videos?"
    _KEY = glob.config['botmaster']['default_bots']['luise']['ytkey']
    url = f"{_BASE_URL}id={vid}&part={','.join(parts)}&key={_KEY}"
    res = Session().get(url)
    if not res.ok:
        msg = None
        try:
            js = res.json()
            msg = js["error"]["message"]
        except ValueError:
            msg = "Antwort nicht valide"
        finally:
            raise ConnectionRefusedError(f"Youtube-API hat die Verbindung verweigert, Status: {res.status_code}, {msg}")

    js = res.json()
    if not js["items"]:
        raise VideoNotFoundError(f"Video mit der ID {vid} existiert nicht.")

    return js["items"][0]


def check_valid(vid):
    try:
        lookup_video(vid)
    except (ConnectionRefusedError, VideoNotFoundError):
        return False

    return True


def check_db():
    ret = {}
    with glob.db.context as session:
        for i in session.query(Song.video_id).all():
            ret[i] = check_valid(i)

    return ret

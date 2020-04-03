from requests import Session
from websockets import Origin
from websockets.client import connect

from chatbot import glob


class PreparedConnection:
    def __init__(self, channel="test", position=0, _config=None, url_opts=None):
        if _config is None:
            _config = glob.config
        if url_opts is None:
            url_opts = dict()
        url_opts.update({"channel": channel, "position": position})
        url_opts_str = "&".join(f"{i}={url_opts[i]}" for i in url_opts)
        self.connection_opts = _config["connection"]
        opt = self.connection_opts
        self.ws_url = f"{opt['protocoll']['ws']}://{opt['host']}{opt['path']}?{url_opts_str}"
        self.user_opts = _config["user"]
        self.http_url = f"{opt['protocoll']['http']}://{opt['host']}"

        self.cookie = self._obtain_cookie()

    def connect(self):
        return connect(self.ws_url, extra_headers={"Cookie": self.cookie}, origin=Origin(self.http_url))

    def _obtain_cookie(self):
        ses = Session()
        login_url = self.http_url + self.connection_opts["login"]
        ses.post(login_url, data=self.user_opts)
        return "; ".join(f"{i.name}={i.value}" for i in ses.cookies)

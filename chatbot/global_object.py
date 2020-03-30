from chatbot.bots.botmaster import BotMaster
from chatbot.connection.chat import Chat
from chatbot.interface.bridge import Bridge


class Global:
    def __init__(self):
        self._config = None
        self._bridge = None
        self._chat = None
        self._botmaster = None

    @property
    def config(self):
        if self._config is None:
            raise RuntimeError("Global object is not configured.")
        return self._config

    @config.setter
    def config(self, value):
        if self._config is not None:
            raise RuntimeError("Global object is alread configured.")
        self._config = value

    @property
    def bridge(self):
        if self._bridge is None:
            self._bridge = Bridge()
        return self._bridge

    @property
    def chat(self):
        if self._chat is None:
            self._chat = Chat(self.bridge, self.config)
        return self._chat

    @property
    def botmaster(self):
        if self._botmaster is None:
            self._botmaster = BotMaster(self.bridge, self.config)
        return self._botmaster

    def start_all(self):
        """ Starts all parts in the correct order. """
        # Reading starts them
        _ = self.chat
        _ = self.botmaster

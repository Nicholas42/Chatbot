from logging import getLogger, Logger

from .config import Config
from .global_object import Global

module_logger: Logger = getLogger("chatbot")
glob = Global()

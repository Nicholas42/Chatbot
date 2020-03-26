from .config import Config
from logging import getLogger, Logger

module_logger: Logger = getLogger("chatbot")
config: Config = Config()
